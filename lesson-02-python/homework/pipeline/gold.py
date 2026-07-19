"""Gold stage — three analytics tables built from silver.

TODO (Завдання 4, 5, 6): реалізуйте три функції нижче.
Контракт: див. CONTRACTS.md → "gold repo_activity", "gold activity_per_minute",
"gold push_commits_by_repo". Усі лічильники приводьте до Int64 (.cast(pl.Int64)),
щоб схема результату була стабільною.

  * build_repo_activity:        кількість подій + кількість унікальних типів на repo
  * build_activity_per_minute:  кількість подій по хвилинах (.dt.truncate("1m"))
  * build_push_commits_by_repo: тільки PushEvent — кількість пушів і сума commit_count на repo
"""

from __future__ import annotations

import polars as pl
import os

from . import config
from pathlib import Path


def build_repo_activity(silver: pl.DataFrame) -> pl.DataFrame:

    repo_activity = (silver.group_by("repo_name").agg(
        [pl.len().cast(pl.Int64).alias("event_count"),
        pl.col("event_type").n_unique().cast(pl.Int64).alias("distinct_event_types")]
        ).sort("event_count", descending=True))
    
    Path(config.GOLD_REPO_ACTIVITY).parent.mkdir(parents=True, exist_ok=True)

    repo_activity.write_parquet(config.GOLD_REPO_ACTIVITY) 

    size_mb = os.path.getsize(config.GOLD_REPO_ACTIVITY) / 1_000_000
    print(f"[gold_repo_activity] saved {os.path.basename(config.GOLD_REPO_ACTIVITY)} {size_mb:.1f} MB, {repo_activity.height} rows")

    return repo_activity


def build_activity_per_minute(silver: pl.DataFrame) -> pl.DataFrame:
    raise NotImplementedError("Завдання 5: реалізуйте activity_per_minute згідно з CONTRACTS.md")


def build_push_commits_by_repo(silver: pl.DataFrame) -> pl.DataFrame:
    raise NotImplementedError("Завдання 6: реалізуйте push_commits_by_repo згідно з CONTRACTS.md")
