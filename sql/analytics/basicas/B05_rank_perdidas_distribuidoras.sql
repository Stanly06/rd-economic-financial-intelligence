-- B5 (RANK). ¿Qué distribuidora eléctrica tiene más pérdidas de energía? (último mes publicado)
WITH ultimo_mes AS (
    SELECT distributor, reference_month, losses_pct
    FROM rd_economic_intelligence.gold.electricity_metrics
    WHERE distributor <> 'Total EDE'
      AND reference_month = (SELECT MAX(reference_month) FROM rd_economic_intelligence.gold.electricity_metrics)
)
SELECT RANK() OVER (ORDER BY losses_pct DESC) AS puesto,
       distributor                            AS distribuidora,
       date_format(reference_month, 'yyyy-MM') AS mes,
       ROUND(losses_pct, 1)                   AS perdidas_pct
FROM ultimo_mes
ORDER BY puesto;
