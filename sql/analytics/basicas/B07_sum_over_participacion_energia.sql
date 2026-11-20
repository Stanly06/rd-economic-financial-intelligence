-- B7 (SUM() OVER ()). ¿Qué porcentaje de la energía comprada se lleva cada distribuidora? (último mes)
WITH ultimo_mes AS (
    SELECT distributor, reference_month, energy_bought_gwh
    FROM rd_economic_intelligence.gold.electricity_metrics
    WHERE distributor <> 'Total EDE'
      AND reference_month = (SELECT MAX(reference_month) FROM rd_economic_intelligence.gold.electricity_metrics)
)
SELECT distributor                                                       AS distribuidora,
       date_format(reference_month, 'yyyy-MM')                           AS mes,
       ROUND(energy_bought_gwh, 1)                                       AS energia_comprada_gwh,
       ROUND(SUM(energy_bought_gwh) OVER (), 1)                          AS total_gwh,
       ROUND(energy_bought_gwh / SUM(energy_bought_gwh) OVER () * 100, 1) AS participacion_pct
FROM ultimo_mes
ORDER BY participacion_pct DESC;
