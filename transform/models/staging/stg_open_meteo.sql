WITH raw_weather AS (
    SELECT * FROM {{ source('raw', 'open_meteo') }}
)

SELECT
    CAST(time AS TIMESTAMP) AS time_hour,
    CAST(temperature_2m AS DOUBLE) AS temperature_celsius
FROM raw_weather
WHERE temperature_2m IS NOT NULL