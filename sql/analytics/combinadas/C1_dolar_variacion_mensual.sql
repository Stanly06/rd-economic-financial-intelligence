-- C1. ¿Cómo se movió el dólar cada mes de 2026 y cuál fue el mes de mayor depreciación del peso?
WITH tasa_diaria AS (                       -- Paso 1: tasa de venta diaria del dólar
    SELECT rate_date, rate
    FROM rd_economic_intelligence.gold.exchange_rate_metrics
    WHERE rate_type = 'sell' AND currency_pair = 'USD/DOP'
),
promedio_mensual AS (                       -- Paso 2: promedio de cada mes
    SELECT date_trunc('MONTH', rate_date) AS mes,
           ROUND(AVG(rate), 4)            AS tasa_promedio,
           COUNT(*)                       AS dias_habiles
    FROM tasa_diaria
    GROUP BY date_trunc('MONTH', rate_date)
),
con_mes_anterior AS (                       -- Paso 3: traer el mes anterior con LAG
    SELECT mes, tasa_promedio, dias_habiles,
           LAG(tasa_promedio) OVER (ORDER BY mes) AS tasa_mes_anterior
    FROM promedio_mensual
)
SELECT date_format(mes, 'yyyy-MM')                                        AS mes,
       tasa_promedio,
       tasa_mes_anterior,
       ROUND((tasa_promedio / tasa_mes_anterior - 1) * 100, 2)            AS variacion_pct,
       RANK() OVER (ORDER BY tasa_promedio / tasa_mes_anterior DESC)     AS ranking_depreciacion
FROM con_mes_anterior
WHERE year(mes) = 2026
ORDER BY mes;
