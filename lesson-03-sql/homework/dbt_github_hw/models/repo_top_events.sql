-- =====================================================================
-- TASK 2 — repo_top_events (12 балів). Специфікація: ../../MODELS.md → «repo_top_events».
-- TOP-5 репозиторіїв за кількістю подій у кожному event_type: ROW_NUMBER() + QUALIFY.
-- Контракт колонок нижче; заглушка повертає 0 рядків.
-- =====================================================================
WITH event_count_cte as (
    SELECT 
        event_type,
        repo_name,
        count(*) as event_count
    FROM {{ ref('stg_events') }} 
    GROUP BY event_type, repo_name)
        SELECT event_type,
            repo_name, event_count, 
            ROW_NUMBER() OVER (PARTITION BY event_type ORDER BY event_count DESC, repo_name) AS type_rank
        FROM event_count_cte
        QUALIFY type_rank <= 5
