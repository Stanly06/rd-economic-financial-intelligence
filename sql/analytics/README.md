# Análisis SQL sobre la capa Gold

Diecisiete preguntas de negocio respondidas con **SQL en Databricks** sobre las tablas Gold del catálogo `rd_economic_intelligence`. Cada consulta usa **CTE** (`WITH … AS`) y **funciones de ventana** (`OVER`, `LAG`, `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `ROWS BETWEEN`).

- **Notebook con explicación paso a paso y resultados:** [`src/analytics/09_SQL_Analytics.ipynb`](../../src/analytics/09_SQL_Analytics.ipynb). En Databricks, conéctalo a Serverless y presiona Run all: cada consulta muestra su tabla de resultados debajo.
- **Consultas sueltas:** [`basicas/`](basicas) (una función a la vez) y [`combinadas/`](combinadas) (varias funciones por consulta). Se pueden abrir en el editor SQL de Databricks.

## Parte B · Una función a la vez

| # | Función | Archivo | Pregunta de negocio | Resultado (19-nov-2026) |
|---|---|---|---|---|
| B1 | CTE | [`B01`](basicas/B01_cte_dolar_promedio_anual.sql) | ¿Cuál fue la tasa promedio del dólar cada año desde 2020? | De RD$56.58 (2020) a RD$61.99 (2025); 2026 va en RD$60.31. |
| B2 | `LAG` | [`B02`](basicas/B02_lag_gasolina_semana_a_semana.sql) | ¿Cuánto cambió la gasolina premium semana a semana? | De RD$338 a RD$353 en 10 semanas. |
| B3 | `LEAD` | [`B03`](basicas/B03_lead_inflacion_mes_siguiente.sql) | ¿En qué meses de 2026 la inflación del mes siguiente fue mayor? | Subió de marzo a junio (5.67 %), luego bajó. |
| B4 | `ROW_NUMBER` | [`B04`](basicas/B04_row_number_ultimo_precio_combustible.sql) | ¿Cuál es el precio más reciente de cada combustible? | Kerosene RD$383 el más caro; GLP RD$135 el más barato. |
| B5 | `RANK` | [`B05`](basicas/B05_rank_perdidas_distribuidoras.sql) | ¿Qué distribuidora eléctrica tiene más pérdidas? | Edeeste 60.2 %, Edesur 36.2 %, Edenorte 30.2 % (julio). |
| B6 | `DENSE_RANK` | [`B06`](basicas/B06_dense_rank_diferencia_precios.sql) | ¿Qué productos tienen más diferencia de precio entre establecimientos? | Auyama: 77 % más cara en colmados que en supermercados grandes. |
| B7 | `SUM() OVER ()` | [`B07`](basicas/B07_sum_over_participacion_energia.sql) | ¿Qué % de la energía comprada se lleva cada distribuidora? | Edeeste 37.4 %, Edesur 33.0 %, Edenorte 29.6 %. |
| B8 | Acumulado | [`B08`](basicas/B08_acumulado_energia_2026.sql) | ¿Cuánta energía han comprado las EDE en 2026? | 12,072 GWh de enero a julio. |
| B9 | Promedio móvil | [`B09`](basicas/B09_promedio_movil_inflacion.sql) | ¿Cuál es el promedio móvil de 3 meses de la inflación? | De 3.90 % (oct-2025) a 5.13 % (oct-2026). |
| B10 | `FIRST_VALUE` | [`B10`](basicas/B10_first_value_dolar_desde_enero.sql) | ¿Cuánto ha cambiado el dólar desde el primer día del año? | −4.31 % al 13 de noviembre. |
| B11 | `NTILE` | [`B11`](basicas/B11_ntile_cuartiles_agricultura.sql) | ¿Qué productos agrícolas están en el 25 % que más subió? | 23 productos, con alzas de 9.5 % a 56.6 %. |

## Parte C · Preguntas combinadas

| # | Archivo | Pregunta de negocio | Funciones |
|---|---|---|---|
| C1 | [`C1_dolar_variacion_mensual.sql`](combinadas/C1_dolar_variacion_mensual.sql) | ¿Cómo se movió el dólar cada mes de 2026 y cuándo se depreció más el peso? | CTE, `LAG`, `RANK` |
| C2 | [`C2_combustibles_ranking_12_semanas.sql`](combinadas/C2_combustibles_ranking_12_semanas.sql) | ¿Qué combustibles subieron más en 12 semanas y cuántas semanas subieron? | CTE, `LAG(…, 12)`, `SUM … ROWS BETWEEN`, `RANK` vs `DENSE_RANK` vs `ROW_NUMBER` |
| C3 | [`C3_inflacion_top_grupos_por_anio.sql`](combinadas/C3_inflacion_top_grupos_por_anio.sql) | ¿Qué grupos de gasto tuvieron la inflación interanual más alta cada año? | CTE, `LAG`, `ROW_NUMBER`, `DENSE_RANK … PARTITION BY` |
| C4 | [`C4_inflacion_vs_dolar.sql`](combinadas/C4_inflacion_vs_dolar.sql) | ¿La inflación y el dólar se mueven juntos? | 4 CTE encadenadas, `JOIN`, `AVG … ROWS BETWEEN`, `QUALIFY` |
| C5 | [`C5_canasta_por_quintil.sql`](combinadas/C5_canasta_por_quintil.sql) | ¿Cuánto cuesta la canasta familiar por quintil de ingreso y cuánto subió en un año? | CTE, `LAG`, `MIN() OVER ()`, `RANK` |
| C6 | [`C6_agricultura_top_alzas_por_rubro.sql`](combinadas/C6_agricultura_top_alzas_por_rubro.sql) | ¿Qué productos agrícolas subieron más en el último año dentro de cada rubro? | CTE, `DENSE_RANK`, `AVG/COUNT … OVER (PARTITION BY)` |

## Funciones usadas

| Función | Qué hace |
|---|---|
| `WITH nombre AS (…)` (CTE) | Tabla temporal con nombre que solo existe durante la consulta. Permite resolver el problema por pasos. |
| `OVER (PARTITION BY … ORDER BY …)` | Calcula sobre un grupo de filas sin agruparlas: cada fila conserva su detalle. `PARTITION BY` define el grupo y `ORDER BY` el orden dentro del grupo. |
| `LAG(col, n)` / `LEAD(col, n)` | Valor de `n` filas antes o después: semana anterior, mismo mes del año pasado. |
| `ROW_NUMBER()` | Numera 1, 2, 3… sin repetir. Sirve para quedarse con el registro más reciente. |
| `RANK()` | Repite el puesto en empates y salta el siguiente: 1, 1, 3. |
| `DENSE_RANK()` | Repite el puesto en empates sin saltar: 1, 1, 2. |
| `ROWS BETWEEN n PRECEDING AND CURRENT ROW` | Ventana móvil: promedio de 3 meses o suma de 12 semanas. |
| `QUALIFY` | Filtra por el resultado de una función de ventana. |
| `FIRST_VALUE()` | Primer valor de la ventana: sirve como punto de partida fijo. |
| `NTILE(n)` | Reparte las filas en `n` grupos del mismo tamaño (cuartiles, deciles). |
| `SUM() OVER ()` | Total de toda la tabla en cada fila, para calcular participación %. |

## Resultados de las preguntas combinadas (corrida del 19 de noviembre de 2026)

**C1. Dólar 2026.** El peso se apreció de enero a agosto (de RD$63.51 a RD$58.68 de promedio mensual). En octubre el dólar subió 3.17 %, la mayor alza del año.

**C2. Combustibles, últimas 12 semanas** (última semana publicada: 25-sep-2026). El empate en 9 semanas de subida muestra la diferencia entre las tres funciones de ranking:

| Combustible | Cambio 12 sem. | Semanas con subida | `RANK` | `DENSE_RANK` | `ROW_NUMBER` |
|---|---|---|---|---|---|
| AVTUR | +41.18 % | 9 | 1 | 1 | 1 |
| KEROSENE | +40.81 % | 9 | 1 | 1 | 2 |
| FUEL OIL | +15.79 % | 8 | 3 | 2 | 3 |
| GASOIL REGULAR | +5.06 % | 5 | 4 | 3 | 4 |
| GASOLINA REGULAR | +3.93 % | 5 | 4 | 3 | 5 |
| GLP | −1.46 % | 0 | 8 | 5 | 8 |

**C3. Inflación por grupo de gasto.** Primer lugar de cada año: 2026 (a octubre) Transporte 9.30 %; 2025 Alimentos y Bebidas 8.19 %; 2024 Bebidas Alcohólicas y Tabaco 5.93 %; 2023 Restaurantes y Hoteles 7.13 %; 2022 Alimentos y Bebidas 11.19 %; 2021 Transporte 16.24 %.

**C4. Inflación vs dólar.** En 2026 se separan: la inflación interanual se mantiene entre 4.6 % y 5.7 % mientras el dólar baja frente al año anterior (−5.8 % en agosto y septiembre). La brecha llega a 10.9 puntos.

**C5. Canasta por quintil (octubre 2026).**

| Quintil | Canasta (RD$) | Hace 12 meses (RD$) | Aumento | Veces el quintil 1 |
|---|---|---|---|---|
| Quintil 1 | 29,972.34 | 28,618.93 | +4.73 % | 1.00 |
| Quintil 2 | 39,120.01 | 37,262.10 | +4.99 % | 1.31 |
| Quintil 3 | 46,145.95 | 43,958.65 | +4.98 % | 1.54 |
| Quintil 4 | 53,389.75 | 50,925.40 | +4.84 % | 1.78 |
| Quintil 5 | 81,727.62 | 77,617.32 | +5.30 % | 2.73 |

**C6. Agricultura, mayores alzas interanuales (minorista, octubre 2026).** Mango Gota de Oro +56.6 %, repollo +46.5 %, ajo criollo +39.8 %, guandul verde +34.4 % y yautía blanca +31.7 %. Raíces y tubérculos es el rubro con mayor alza promedio (12.79 %).

Los resultados cambian cada lunes, cuando el Job de Lakeflow actualiza las tablas Gold.
