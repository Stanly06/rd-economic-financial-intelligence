-- C5. ¿Cuánto cuesta la canasta familiar por quintil de ingreso y cuánto subió en un año?
WITH quintiles AS (                            -- Paso 1: costo mensual de la canasta por quintil
    SELECT segment AS quintil, reference_month, basket_cost_dop
    FROM rd_economic_intelligence.gold.cost_of_living_metrics
    WHERE segment_type = 'income_quintile'
),
con_anio_anterior AS (                         -- Paso 2: costo de hace 12 meses con LAG
    SELECT quintil, reference_month, basket_cost_dop,
           LAG(basket_cost_dop, 12) OVER (PARTITION BY quintil ORDER BY reference_month) AS costo_hace_12m
    FROM quintiles
),
ultimo_mes AS (                                -- Paso 3: solo el mes más reciente
    SELECT * FROM con_anio_anterior
    WHERE reference_month = (SELECT MAX(reference_month) FROM quintiles)
)
SELECT quintil,
       date_format(reference_month, 'yyyy-MM')                                AS mes,
       ROUND(basket_cost_dop, 2)                                             AS costo_canasta_dop,
       ROUND(costo_hace_12m, 2)                                              AS costo_hace_12m_dop,
       ROUND(basket_cost_dop - costo_hace_12m, 2)                            AS aumento_dop,
       ROUND((basket_cost_dop / costo_hace_12m - 1) * 100, 2)                AS aumento_pct,
       ROUND(basket_cost_dop / MIN(basket_cost_dop) OVER (), 2)              AS veces_quintil_1,
       RANK() OVER (ORDER BY basket_cost_dop / costo_hace_12m DESC)          AS ranking_aumento
FROM ultimo_mes
ORDER BY quintil;
