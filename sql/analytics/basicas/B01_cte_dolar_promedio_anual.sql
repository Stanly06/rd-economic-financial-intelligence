-- B1 (CTE). ¿Cuál fue la tasa promedio del dólar cada año desde 2020?
WITH tasa_venta AS (                 -- La CTE guarda un resultado intermedio con nombre
    SELECT year(rate_date) AS anio, rate
    FROM rd_economic_intelligence.gold.exchange_rate_metrics
    WHERE rate_type = 'sell' AND year(rate_date) >= 2020
)
SELECT anio,
       ROUND(AVG(rate), 2) AS tasa_promedio,
       ROUND(MIN(rate), 2) AS tasa_minima,
       ROUND(MAX(rate), 2) AS tasa_maxima,
       COUNT(*)            AS dias_habiles
FROM tasa_venta                      -- Se consulta la CTE como si fuera una tabla
GROUP BY anio
ORDER BY anio;
