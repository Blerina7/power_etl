WITH raw_prices AS (
    SELECT * FROM {{ source('raw', 'entsoe_prices') }}
)

SELECT
    CAST(time AS TIMESTAMP) AS time_hour,
    CAST(price_eur_mwh AS DOUBLE) AS price_eur_mwh,
    CAST(country AS VARCHAR) AS country_code
FROM raw_prices
WHERE price_eur_mwh IS NOT NULL