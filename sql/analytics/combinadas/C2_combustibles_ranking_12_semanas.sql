-- C2. ¿Qué combustibles subieron más en las últimas 12 semanas y cuántas semanas subieron? (RANK vs DENSE_RANK vs ROW_NUMBER)
WITH principales AS (                        -- Paso 1: los combustibles que usa la gente
    SELECT fuel_name, period_start_date, price_dop
    FROM rd_economic_intelligence.gold.fuel_price_metrics
    WHERE fuel_code IN ('gasolina_premium','gasolina_regular','gasoil_optimo',
                        'gasoil_regular','glp','kerosene','avtur','fuel_oil')
),
con_hace_12_semanas AS (                     -- Paso 2: precio de 12 semanas atrás con LAG(…, 12)
    SELECT fuel_name, period_start_date, price_dop,
           LAG(price_dop, 12) OVER (PARTITION BY fuel_name ORDER BY period_start_date) AS precio_hace_12_sem,
           CASE WHEN price_dop > LAG(price_dop) OVER (PARTITION BY fuel_name ORDER BY period_start_date)
                THEN 1 ELSE 0 END                                                          AS subio_esta_semana,
           ROW_NUMBER()       OVER (PARTITION BY fuel_name ORDER BY period_start_date DESC) AS orden_reciente
    FROM principales
),
con_conteo AS (                              -- Paso 3: cuántas de las últimas 12 semanas subió (suma móvil)
    SELECT *,
           SUM(subio_esta_semana) OVER (PARTITION BY fuel_name ORDER BY period_start_date
                                        ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS semanas_con_subida
    FROM con_hace_12_semanas
),
ultima_semana AS (                           -- Paso 4: quedarnos con la semana más reciente
    SELECT fuel_name, period_start_date AS semana, price_dop AS precio_actual, precio_hace_12_sem, semanas_con_subida,
           ROUND(price_dop - precio_hace_12_sem, 2)                        AS cambio_dop,
           ROUND((price_dop / precio_hace_12_sem - 1) * 100, 2)            AS cambio_pct
    FROM con_conteo
    WHERE orden_reciente = 1
)
SELECT fuel_name AS combustible, semana, precio_actual, precio_hace_12_sem, cambio_dop, cambio_pct,
       RANK() OVER (ORDER BY cambio_pct DESC)                AS puesto_por_alza,
       semanas_con_subida,
       RANK()       OVER (ORDER BY semanas_con_subida DESC)   AS rank_subidas,
       DENSE_RANK() OVER (ORDER BY semanas_con_subida DESC)   AS dense_rank_subidas,
       ROW_NUMBER() OVER (ORDER BY semanas_con_subida DESC, cambio_pct DESC) AS row_number_subidas
FROM ultima_semana
ORDER BY semanas_con_subida DESC, cambio_pct DESC;
