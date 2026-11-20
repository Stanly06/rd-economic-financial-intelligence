-- C6. ¿Qué productos agrícolas subieron más en el último año dentro de cada rubro? (Top 3, mercado minorista)
WITH ultimo_mes AS (                           -- Paso 1: el mes más reciente con datos
    SELECT MAX(reference_month) AS mes
    FROM rd_economic_intelligence.gold.agri_price_monthly
),
precios AS (                                   -- Paso 2: precio promedio de todos los mercados por producto
    SELECT a.rubro, a.product, a.unit, a.avg_price_dop, ROUND(a.yoy_pct, 2) AS yoy_pct, a.markets_quoted
    FROM rd_economic_intelligence.gold.agri_price_monthly a
    JOIN ultimo_mes u ON a.reference_month = u.mes
    WHERE a.channel = 'retail' AND a.market = 'Promedio mercados' AND a.yoy_pct IS NOT NULL
),
ranking AS (                                   -- Paso 3: ordenar por alza dentro de cada rubro
    SELECT rubro, product, unit, avg_price_dop, yoy_pct,
           DENSE_RANK() OVER (PARTITION BY rubro ORDER BY yoy_pct DESC)  AS puesto_en_rubro,
           ROUND(AVG(yoy_pct) OVER (PARTITION BY rubro), 2)            AS alza_promedio_rubro,
           COUNT(*) OVER (PARTITION BY rubro)                          AS productos_en_rubro
    FROM precios
)
SELECT rubro, puesto_en_rubro, product AS producto, unit AS unidad,
       ROUND(avg_price_dop, 2) AS precio_promedio_dop, yoy_pct AS alza_interanual_pct,
       alza_promedio_rubro, productos_en_rubro
FROM ranking
WHERE puesto_en_rubro <= 3
ORDER BY rubro, puesto_en_rubro;
