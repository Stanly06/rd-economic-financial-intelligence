-- C3. ¿Qué grupos de gasto tuvieron la inflación interanual más alta cada año? (Top 3 por año)
WITH grupos AS (                              -- Paso 1: índice mensual de cada grupo de gasto
    SELECT series_name AS grupo, reference_month, index_value
    FROM rd_economic_intelligence.gold.inflation_metrics
    WHERE series_type = 'expenditure_group'
),
interanual AS (                               -- Paso 2: índice de hace 12 meses con LAG
    SELECT grupo, reference_month, index_value,
           LAG(index_value, 12) OVER (PARTITION BY grupo ORDER BY reference_month) AS indice_hace_12m
    FROM grupos
),
cierre_anual AS (                             -- Paso 3: inflación interanual de diciembre (o el último mes del año en curso)
    SELECT grupo, year(reference_month) AS anio, reference_month,
           ROUND((index_value / indice_hace_12m - 1) * 100, 2) AS inflacion_interanual_pct,
           ROW_NUMBER() OVER (PARTITION BY grupo, year(reference_month) ORDER BY reference_month DESC) AS ultimo_mes
    FROM interanual
    WHERE indice_hace_12m IS NOT NULL
),
ranking AS (                                  -- Paso 4: ordenar los grupos dentro de cada año
    SELECT anio, date_format(reference_month, 'yyyy-MM') AS mes_cierre, grupo, inflacion_interanual_pct,
           DENSE_RANK() OVER (PARTITION BY anio ORDER BY inflacion_interanual_pct DESC) AS puesto
    FROM cierre_anual
    WHERE ultimo_mes = 1 AND anio >= 2021
)
SELECT * FROM ranking
WHERE puesto <= 3
ORDER BY anio DESC, puesto;
