-- B9 (promedio móvil). ¿Cuál es el promedio móvil de 3 meses de la inflación nacional?
SELECT date_format(reference_month, 'yyyy-MM')                                         AS mes,
       ROUND(yoy_inflation_pct, 2)                                                     AS inflacion_pct,
       ROUND(AVG(yoy_inflation_pct) OVER (ORDER BY reference_month
                                          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS promedio_movil_3m
FROM rd_economic_intelligence.gold.inflation_metrics
WHERE series_type = 'headline'
QUALIFY reference_month >= '2025-10-01'      -- se filtra después de calcular, para que el promedio use los meses anteriores
ORDER BY reference_month;
