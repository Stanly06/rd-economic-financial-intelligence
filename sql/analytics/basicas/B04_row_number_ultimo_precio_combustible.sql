-- B4 (ROW_NUMBER). ¿Cuál es el precio más reciente de cada combustible?
WITH numerados AS (
    SELECT fuel_name, period_start_date, price_dop,
           ROW_NUMBER() OVER (PARTITION BY fuel_name ORDER BY period_start_date DESC) AS n
    FROM rd_economic_intelligence.gold.fuel_price_metrics
    WHERE fuel_code IN ('gasolina_premium','gasolina_regular','gasoil_optimo','gasoil_regular','glp','kerosene')
)
SELECT fuel_name AS combustible, period_start_date AS semana, price_dop AS precio_dop
FROM numerados
WHERE n = 1                          -- n = 1 es la fila más reciente de cada combustible
ORDER BY precio_dop DESC;
