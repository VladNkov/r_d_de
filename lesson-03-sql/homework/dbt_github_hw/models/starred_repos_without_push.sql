-- =====================================================================
-- TASK 5 — starred_repos_without_push (12 балів). Специфікація: ../../MODELS.md → «starred_repos_without_push».
-- Репозиторії зі зіркою (WatchEvent), але без жодного PushEvent: anti-join (NOT EXISTS).
-- Контракт колонок нижче; заглушка повертає 0 рядків.
-- =====================================================================
WITH watch_events AS (
SELECT DISTINCT
    repo_name
FROM {{ ref('stg_events') }} 
WHERE event_type = 'WatchEvent'),
    
push_events AS (
SELECT DISTINCT
    repo_name
FROM {{ ref('stg_events') }}
WHERE event_type = 'PushEvent')

SELECT
    watch_events.repo_name
FROM watch_events 
LEFT JOIN push_events 
    ON watch_events.repo_name = push_events.repo_name
WHERE push_events.repo_name IS NULL

