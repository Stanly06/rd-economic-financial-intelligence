-- B6 (DENSE_RANK). ¿Qué productos de Pro Consumidor tienen más diferencia de precio entre establecimientos? (Top 5)
WITH ultimo AS (
    SELECT product, presentation, min_price_dop, max_price_dop, price_spread_pct, cheapest_segment, most_expensive_segment
    FROM rd_economic_intelligence.gold.consumer_price_metrics
    WHERE reference_month = (SELECT MAX(reference_month) FROM rd_economic_intelligence.gold.consumer_price_metrics)
),
ranking AS (
    SELECT *, DENSE_RANK() OVER (ORDER BY price_spread_pct DESC) AS puesto
    FROM ultimo
)
SELECT puesto, product AS producto, presentation AS presentacion,
       min_price_dop AS precio_min_dop, max_price_dop AS precio_max_dop,
       ROUND(price_spread_pct, 1) AS diferencia_pct, cheapest_segment AS mas_barato_en, most_expensive_segment AS mas_caro_en
FROM ranking
WHERE puesto <= 5
ORDER BY puesto;
