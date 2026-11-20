-- B10 (FIRST_VALUE). ¿Cuánto ha subido o bajado el dólar desde el primer día hábil del año? (cierre de cada mes)
WITH tasa_2026 AS (
    SELECT rate_date, rate,
           FIRST_VALUE(rate) OVER (ORDER BY rate_date) AS tasa_primer_dia
    FROM rd_economic_intelligence.gold.exchange_rate_metrics
    WHERE rate_type = 'sell' AND year(rate_date) = 2026
)
SELECT rate_date                                         AS fecha,
       rate                                              AS tasa,
       tasa_primer_dia,
       ROUND((rate / tasa_primer_dia - 1) * 100, 2)      AS cambio_desde_inicio_pct
FROM tasa_2026
QUALIFY ROW_NUMBER() OVER (PARTITION BY month(rate_date) ORDER BY rate_date DESC) = 1   -- último día hábil de cada mes
ORDER BY fecha;
