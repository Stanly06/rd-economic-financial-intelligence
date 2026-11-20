-- B2 (LAG). ¿Cuánto cambió el precio de la gasolina premium semana a semana? (últimas 10 semanas)
SELECT period_start_date                                                    AS semana,
       price_dop                                                            AS precio_actual,
       LAG(price_dop) OVER (ORDER BY period_start_date)                     AS precio_semana_anterior,
       price_dop - LAG(price_dop) OVER (ORDER BY period_start_date)         AS cambio_dop
FROM rd_economic_intelligence.gold.fuel_price_metrics
WHERE fuel_code = 'gasolina_premium'
ORDER BY semana DESC
LIMIT 10;
