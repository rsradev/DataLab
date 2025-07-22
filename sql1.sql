-- 1. DDL for `actors` table
CREATE TABLE actors (
    actorid INT PRIMARY KEY,
    films JSONB, -- storing array of structs as JSONB
    quality_class TEXT,
    is_active BOOLEAN
);

-- 2. Cumulative population of `actors` table for a given year (replace :input_year)
WITH latest_films AS (
    SELECT *
    FROM actor_films
    WHERE year <= :input_year
),
latest_years AS (
    SELECT actorid, MAX(year) AS latest_year
    FROM latest_films
    GROUP BY actorid
),
actor_film_agg AS (
    SELECT
        af.actorid,
        JSONB_AGG(
            JSONB_BUILD_OBJECT(
                'film', af.film,
                'votes', af.votes,
                'rating', af.rating,
                'filmid', af.filmid
            )
        ) AS films,
        AVG(CASE WHEN af.year = ly.latest_year THEN af.rating END) AS recent_avg_rating,
        BOOL_OR(af.year = EXTRACT(YEAR FROM CURRENT_DATE)) AS is_active
    FROM latest_films af
    JOIN latest_years ly ON af.actorid = ly.actorid
    GROUP BY af.actorid, ly.latest_year
)
INSERT INTO actors (actorid, films, quality_class, is_active)
SELECT
    actorid,
    films,
    CASE
        WHEN recent_avg_rating > 8 THEN 'star'
        WHEN recent_avg_rating > 7 THEN 'good'
        WHEN recent_avg_rating > 6 THEN 'average'
        ELSE 'bad'
    END AS quality_class,
    is_active
FROM actor_film_agg
ON CONFLICT (actorid) DO UPDATE
SET films = EXCLUDED.films,
    quality_class = EXCLUDED.quality_class,
    is_active = EXCLUDED.is_active;

-- 3. DDL for `actors_history_scd` table
CREATE TABLE actors_history_scd (
    actorid INT,
    quality_class TEXT,
    is_active BOOLEAN,
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (actorid, start_date)
);

-- 4. Backfill query for `actors_history_scd` (assumes yearly snapshots in a temp or staging table `actors_by_year`)
WITH snapshots AS (
    SELECT actorid, quality_class, is_active, year,
           MAKE_DATE(year, 1, 1) AS snapshot_date
    FROM actors_by_year
),
ranked_snapshots AS (
    SELECT *,
           LAG(quality_class) OVER (PARTITION BY actorid ORDER BY year) AS prev_quality,
           LAG(is_active) OVER (PARTITION BY actorid ORDER BY year) AS prev_active
    FROM snapshots
),
changes AS (
    SELECT
        actorid,
        quality_class,
        is_active,
        year AS start_year,
        LEAD(year) OVER (PARTITION BY actorid ORDER BY year) - 1 AS end_year
    FROM ranked_snapshots
    WHERE quality_class IS DISTINCT FROM prev_quality
       OR is_active IS DISTINCT FROM prev_active
       OR prev_quality IS NULL
)
INSERT INTO actors_history_scd (actorid, quality_class, is_active, start_date, end_date)
SELECT
    actorid,
    quality_class,
    is_active,
    MAKE_DATE(start_year, 1, 1) AS start_date,
    COALESCE(MAKE_DATE(end_year, 1, 1) - INTERVAL '1 day', DATE '9999-12-31') AS end_date
FROM changes;

-- 5. Incremental update of `actors_history_scd` from latest `actors` snapshot
WITH latest_scd AS (
    SELECT *
    FROM actors_history_scd
    WHERE end_date = DATE '9999-12-31'
),
changes AS (
    SELECT
        a.actorid,
        a.quality_class,
        a.is_active,
        s.quality_class AS prev_quality,
        s.is_active AS prev_active,
        s.start_date AS prev_start_date
    FROM actors a
    LEFT JOIN latest_scd s ON a.actorid = s.actorid
),
to_close AS (
    SELECT
        actorid,
        prev_quality,
        prev_active,
        prev_start_date,
        CURRENT_DATE - INTERVAL '1 day' AS end_date
    FROM changes
    WHERE prev_quality IS NOT NULL
      AND (quality_class IS DISTINCT FROM prev_quality OR is_active IS DISTINCT FROM prev_active)
),
to_insert AS (
    SELECT
        actorid,
        quality_class,
        is_active,
        CURRENT_DATE AS start_date,
        DATE '9999-12-31' AS end_date
    FROM changes
    WHERE prev_quality IS NULL
       OR quality_class IS DISTINCT FROM prev_quality
       OR is_active IS DISTINCT FROM prev_active
)
-- Close old records
UPDATE actors_history_scd
SET end_date = c.end_date
FROM to_close c
WHERE actors_history_scd.actorid = c.actorid
  AND actors_history_scd.start_date = c.prev_start_date;

-- Insert new records
INSERT INTO actors_history_scd (actorid, quality_class, is_active, start_date, end_date)
SELECT * FROM to_insert;
