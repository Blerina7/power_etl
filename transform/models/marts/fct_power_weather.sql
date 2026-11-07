WITH prices AS (
    SELECT * FROM {{ ref('stg_entsoe_prices') }}
),

weather AS (
    SELECT * FROM {{ ref('stg_open_meteo') }}
)

SELECT
    p.time_hour,
    p.country_code,
    p.price_eur_mwh,
    w.temperature_celsius
FROM prices p
LEFT JOIN weather w
    ON p.time_hour = w.time_hour
ORDER BY p.time_hour DESC