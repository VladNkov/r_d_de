"""Silver stage — clean, filter and de-duplicate the bronze events.

TODO (Завдання 2 і 3): реалізуйте build_silver() і write_silver_partitioned().
Контракт: див. CONTRACTS.md → "silver" і "silver partitioned".

build_silver():
  * залиште тільки типи з config.TARGET_EVENT_TYPES
  * приберіть рядки з порожнім/відсутнім repo_name, відсутнім event_id чи created_at
  * гарантуйте унікальність по event_id (.unique(subset=["event_id"]))
  * запишіть у config.SILVER_FILE і поверніть DataFrame

write_silver_partitioned():
  * запишіть silver як Hive-партиціонований датасет за event_type
  * директорія: config.SILVER_PARTITIONED_DIR
  * підказка: df.write_parquet(dir, partition_by="event_type")
"""

from __future__ import annotations
from icecream import ic
from pathlib import Path

import polars as pl
import os

from . import config


def build_silver(bronze: pl.DataFrame) -> pl.DataFrame:

    silver_df = (bronze.filter(pl.col("event_type").is_in(config.TARGET_EVENT_TYPES))
        .filter(pl.col("repo_name").is_not_null())
        .filter(pl.col("repo_name") != "")
        .filter(pl.col("event_id").is_not_null())
        .filter(pl.col("created_at").is_not_null())
        .unique(subset=["event_id"]))
    
    # ic(silver_df.head(5))

    Path(config.SILVER_FILE).parent.mkdir(parents=True, exist_ok=True)

    silver_df.write_parquet(config.SILVER_FILE)

    size_mb = os.path.getsize(config.SILVER_FILE) / 1_000_000
    print(f"[silver] saved {os.path.basename(config.SILVER_FILE)} {size_mb:.1f} MB, {silver_df.height} rows")

    return silver_df



def write_silver_partitioned(silver: pl.DataFrame) -> None:
    # raise NotImplementedError("Завдання 3: запишіть партиціонований silver за event_type")

    output_dir = Path(config.SILVER_PARTITIONED_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    silver.write_parquet(output_dir, partition_by="event_type")

    n_partitions = len(list(output_dir.glob("event_type=*")))
    size_mb = sum(f.stat().st_size for f in output_dir.rglob("*.parquet")) / 1_000_000
    print(f"[silver_partitioned] saved {n_partitions} partitions in {output_dir}, "f"{size_mb:.1f} MB, {silver.height} rows")
