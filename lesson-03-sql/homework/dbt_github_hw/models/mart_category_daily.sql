-- =====================================================================
-- TASK 6 — mart_category_daily (20 балів). Специфікація: ../../MODELS.md → «mart_category_daily».
-- Широка вітрина: multi-join stg_events + event_categories + calendar, агрегація по (день × категорія).
-- Контракт колонок нижче; заглушка повертає 0 рядків.
-- =====================================================================
--**Що:** широка вітрина — об'єднує події з **двома** довідниками в одну таблицю
--(це і є приклад multi-join). Грануляція: один рядок на `(event_date, category)`.

--Колонки:** `event_date`, `is_weekend`, `category`, `events` (кількість),
--`distinct_repos` (`count(DISTINCT repo_name)`), `distinct_actors` (`count(DISTINCT actor_login)`).

--**Патерн:** 3-way join `stg_events` + `event_categories` (по `event_type`) +
--`calendar` (по `event_date = day`), далі `GROUP BY event_date, is_weekend, category`. 

--Checkpoint:** **42 рядки** (14 днів × 3 категорії).
SELECT
    event_date,
    is_weekend,
    category,
    COUNT(*) AS events,
    COUNT(DISTINCT repo_name) AS distinct_repos,
    COUNT(DISTINCT actor_login)AS distinct_actors
FROM {{ ref('stg_events') }} AS se
JOIN {{ ref('calendar') }} AS c
    ON se.event_date = c.day
JOIN {{ ref('event_categories') }} AS ec
    ON se.event_type = ec.event_type
GROUP BY se.event_date, c.is_weekend, ec.category
ORDER BY se.event_date, ec.category
