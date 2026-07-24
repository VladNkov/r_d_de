# Спочатку перейди в локальний проєкт

cd ~/Documents/gitProjects/r_d_de   

# Перевір гілку та зміни:

git status

# Якщо незакомічених змін немає, перемкнись на main:

git switch main

# Отримай нові зміни

git fetch upstream
git pull upstream main

# потім створи окрему гілку для ДЗ

git switch -c homework-03

# переходжу в папку з дз

cd lesson-03-sql/homework

# віртуальне середовище

source .venv/bin/activate

# Залежності (один раз — ця директорія має власне pyproject.toml/uv.lock)

uv sync

# запуск моделі stg_events

uv run dbt build --profiles-dir . --select stg_events

# запуск моделі stg_events, якщо з незрозумілих причин запускаються ще й інші

uv run dbt build --profiles-dir . --select stg_events --indirect-selection=cautious

# DuckDB CLI

brew install duckdb

# Видалити файл із git add але залишити файл та зміни

git restore --staged NOTES.md
