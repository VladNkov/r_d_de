"""github_archive_daily — ВАШ DAG. Специфікація: ../SPEC.md → «DAG».

Готові ETL-цеглинки вже є — імпортуйте і викликайте їх у задачах (не переписуйте):

    from include.gh_etl import download, validate, load_to_duckdb, summarize
    from gh_sensor import GHArchiveSensor   # ваш custom sensor із plugins/

Що треба зібрати (деталі й бали — у SPEC.md):
  * DAG `github_archive_daily`, розклад «щодня о 06:00 UTC», catchup=False;
  * усі задачі працюють із logical date {{ ds }}, а не datetime.now() — це дає
    ідемпотентність і коректний backfill;
  * граф:
        check_availability -> download_archive -> validate_file
            -> load_to_duckdb -> notify_completion
  * download_archive кладе шлях у XCom; validate_file і load_to_duckdb беруть його з XCom;
  * шляхи (дано):
        DB_PATH     = "/opt/airflow/data/github_analytics.duckdb"
        LANDING_DIR = "/opt/airflow/data/landing"

Перевірка: `airflow dags test github_archive_daily 2024-01-14` має пройти всі задачі;
наскрізно — `./verify.sh` із кореня homework/.
"""

from __future__ import annotations
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from include.gh_etl import download, validate, load_to_duckdb, summarize
from plugins.gh_sensor import GHArchiveSensor


DB_PATH     = "/opt/airflow/data/github_analytics.duckdb"
LANDING_DIR = "/opt/airflow/data/landing"


def _download(ds, **context):
  return download(ds, LANDING_DIR)

def _validate(**context):
  path = context['ti'].xcom_pull(task_ids='download_archive')
  validate(path)

def _load(ds, **context):
    path = context["ti"].xcom_pull(task_ids="download_archive")
    load_to_duckdb(path, ds, DB_PATH)

def _notify(ds, **context):
    summarize(ds, DB_PATH)


with DAG(
    dag_id="github_archive_daily",
    schedule="0 6 * * *",
    start_date=datetime(2024,1,14),
    catchup=False,
    tags=["github", "homework"],
) as dag:
  check_availability = GHArchiveSensor(
    task_id='check_availability',
    hour=14,
    timeout=600,
    poke_interval=60,
    mode='reschedule'
    )
  
  download_archive = PythonOperator(task_id='download_archive', python_callable=_download)

  validate_file = PythonOperator(task_id='validate_file', python_callable=_validate)

  load_to_duckdb_task = PythonOperator(task_id='load_to_duckdb', python_callable=_load)

  notify_completion = PythonOperator(task_id='notify_completion', python_callable=_notify)

  check_availability >> download_archive >> validate_file >> load_to_duckdb_task >> notify_completion



