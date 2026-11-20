-- P4. ¿La inflación y el dólar se mueven juntos? Comparación interanual de los últimos 24 meses
WITH ipc AS (                                  -- Paso 1: inflación interanual nacional (calculada con LAG)
    SELECT reference_month AS mes,
           ROUND((index_value / LAG(index_value, 12) OVER (ORDER BY reference_month) - 1) * 100, 2) AS inflacion_yoy_pct
    FROM rd_economic_intelligence.gold.inflation_metrics
    WHERE series_type = 'headline'
),
dolar_mensual AS (                             -- Paso 2: tasa de venta promedio de cada mes
    SELECT date_trunc('MONTH', rate_date) AS mes, AVG(rate) AS tasa_promedio
    FROM rd_economic_intelligence.gold.exchange_rate_metrics
    WHERE rate_type = 'sell'
    GROUP BY date_trunc('MONTH', rate_date)
),
dolar_yoy AS (                                 -- Paso 3: variación interanual del dólar con LAG
    SELECT mes, ROUND(tasa_promedio, 2) AS tasa_promedio,
           ROUND((tasa_promedio / LAG(tasa_promedio, 12) OVER (ORDER BY mes) - 1) * 100, 2) AS dolar_yoy_pct
    FROM dolar_mensual
),
unidos AS (                                    -- Paso 4: unir ambas series por mes
    SELECT i.mes, i.inflacion_yoy_pct, d.tasa_promedio, d.dolar_yoy_pct
    FROM ipc i JOIN dolar_yoy d ON i.mes = d.mes
    WHERE i.inflacion_yoy_pct IS NOT NULL
)
SELECT date_format(mes, 'yyyy-MM') AS mes,
       inflacion_yoy_pct,
       dolar_yoy_pct,
       ROUND(inflacion_yoy_pct - dolar_yoy_pct, 2)                                         AS brecha_pp,
       ROUND(AVG(inflacion_yoy_pct) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS inflacion_prom_3m,
       ROUND(AVG(dolar_yoy_pct)     OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS dolar_prom_3m
FROM unidos
QUALIFY ROW_NUMBER() OVER (ORDER BY mes DESC) <= 24
ORDER BY mes;
