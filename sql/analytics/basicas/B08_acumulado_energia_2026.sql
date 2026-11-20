-- B8 (acumulado). ¿Cuánta energía han comprado las EDE en lo que va de 2026, mes a mes?
SELECT date_format(reference_month, 'yyyy-MM')                                    AS mes,
       ROUND(energy_bought_gwh, 1)                                                AS energia_del_mes_gwh,
       ROUND(SUM(energy_bought_gwh) OVER (ORDER BY reference_month
                                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 1) AS acumulado_gwh
FROM rd_economic_intelligence.gold.electricity_metrics
WHERE distributor = 'Total EDE' AND year(reference_month) = 2026
ORDER BY reference_month;
