-- B3 (LEAD). En 2026, ¿en qué meses la inflación del mes siguiente fue mayor que la del mes actual?
WITH ipc AS (
    SELECT reference_month, yoy_inflation_pct
    FROM rd_economic_intelligence.gold.inflation_metrics
    WHERE series_type = 'headline'
)
SELECT date_format(reference_month, 'yyyy-MM')                              AS mes,
       ROUND(yoy_inflation_pct, 2)                                          AS inflacion_pct,
       ROUND(LEAD(yoy_inflation_pct) OVER (ORDER BY reference_month), 2)    AS inflacion_mes_siguiente,
       CASE WHEN LEAD(yoy_inflation_pct) OVER (ORDER BY reference_month) IS NULL THEN 'Aún sin dato'
            WHEN LEAD(yoy_inflation_pct) OVER (ORDER BY reference_month) > yoy_inflation_pct THEN 'Sube'
            ELSE 'Baja o igual' END                                         AS que_pasa_despues
FROM ipc
WHERE reference_month >= '2025-12-01'
ORDER BY reference_month;
