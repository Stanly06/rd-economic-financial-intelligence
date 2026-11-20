-- B11 (NTILE). Dividir los productos agrícolas en 4 grupos según su alza anual: ¿cuáles están en el 25 % que más subió?
WITH precios AS (
    SELECT rubro, product, ROUND(yoy_pct, 2) AS alza_pct
    FROM rd_economic_intelligence.gold.agri_price_monthly
    WHERE channel = 'retail' AND market = 'Promedio mercados' AND yoy_pct IS NOT NULL
      AND reference_month = (SELECT MAX(reference_month) FROM rd_economic_intelligence.gold.agri_price_monthly)
),
cuartiles AS (
    SELECT *, NTILE(4) OVER (ORDER BY alza_pct DESC) AS cuartil   -- 1 = el 25 % que más subió
    FROM precios
)
SELECT cuartil, rubro, product AS producto, alza_pct
FROM cuartiles
WHERE cuartil = 1                    -- solo el 25 % de productos que más subió
ORDER BY alza_pct DESC;
