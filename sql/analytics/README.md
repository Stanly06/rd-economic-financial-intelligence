# Análisis SQL sobre la capa Gold

Seis preguntas de negocio respondidas con **SQL en Databricks** sobre las tablas Gold del catálogo `rd_economic_intelligence`. Cada consulta usa **CTE** (`WITH … AS`) y **funciones de ventana** (`OVER`, `LAG`, `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `ROWS BETWEEN`).

- **Notebook con explicación paso a paso y resultados:** [`src/analytics/09_SQL_Analytics.ipynb`](../../src/analytics/09_SQL_Analytics.ipynb). En Databricks, conéctalo a Serverless y presiona Run all: cada consulta muestra su tabla de resultados debajo.
- **Consultas sueltas:** los archivos `.sql` de esta carpeta. Se pueden abrir en el editor SQL de Databricks.

| # | Archivo | Pregunta de negocio | Funciones |
|---|---|---|---|
| 1 | [`01_dolar_variacion_mensual.sql`](01_dolar_variacion_mensual.sql) | ¿Cómo se movió el dólar cada mes de 2026 y cuándo se depreció más el peso? | CTE, `LAG`, `RANK` |
| 2 | [`02_combustibles_ranking_12_semanas.sql`](02_combustibles_ranking_12_semanas.sql) | ¿Qué combustibles subieron más en 12 semanas y cuántas semanas subieron? | CTE, `LAG(…, 12)`, `SUM … ROWS BETWEEN`, `RANK` vs `DENSE_RANK` vs `ROW_NUMBER` |
| 3 | [`03_inflacion_top_grupos_por_anio.sql`](03_inflacion_top_grupos_por_anio.sql) | ¿Qué grupos de gasto tuvieron la inflación interanual más alta cada año? | CTE, `LAG`, `ROW_NUMBER`, `DENSE_RANK … PARTITION BY` |
| 4 | [`04_inflacion_vs_dolar.sql`](04_inflacion_vs_dolar.sql) | ¿La inflación y el dólar se mueven juntos? | 4 CTE encadenadas, `JOIN`, `AVG … ROWS BETWEEN`, `QUALIFY` |
| 5 | [`05_canasta_por_quintil.sql`](05_canasta_por_quintil.sql) | ¿Cuánto cuesta la canasta familiar por quintil de ingreso y cuánto subió en un año? | CTE, `LAG`, `MIN() OVER ()`, `RANK` |
| 6 | [`06_agricultura_top_alzas_por_rubro.sql`](06_agricultura_top_alzas_por_rubro.sql) | ¿Qué productos agrícolas subieron más en el último año dentro de cada rubro? | CTE, `DENSE_RANK`, `AVG/COUNT … OVER (PARTITION BY)` |

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

## Resultados (corrida del 19 de noviembre de 2026)

**1. Dólar 2026.** El peso se apreció de enero a agosto (de RD$63.51 a RD$58.68 de promedio mensual). En octubre el dólar subió 3.17 %, la mayor alza del año.

**2. Combustibles, últimas 12 semanas** (última semana publicada: 25-sep-2026). El empate en 9 semanas de subida muestra la diferencia entre las tres funciones de ranking:

| Combustible | Cambio 12 sem. | Semanas con subida | `RANK` | `DENSE_RANK` | `ROW_NUMBER` |
|---|---|---|---|---|---|
| AVTUR | +41.18 % | 9 | 1 | 1 | 1 |
| KEROSENE | +40.81 % | 9 | 1 | 1 | 2 |
| FUEL OIL | +15.79 % | 8 | 3 | 2 | 3 |
| GASOIL REGULAR | +5.06 % | 5 | 4 | 3 | 4 |
| GASOLINA REGULAR | +3.93 % | 5 | 4 | 3 | 5 |
| GLP | −1.46 % | 0 | 8 | 5 | 8 |

**3. Inflación por grupo de gasto.** Primer lugar de cada año: 2026 (a octubre) Transporte 9.30 %; 2025 Alimentos y Bebidas 8.19 %; 2024 Bebidas Alcohólicas y Tabaco 5.93 %; 2023 Restaurantes y Hoteles 7.13 %; 2022 Alimentos y Bebidas 11.19 %; 2021 Transporte 16.24 %.

**4. Inflación vs dólar.** En 2026 se separan: la inflación interanual se mantiene entre 4.6 % y 5.7 % mientras el dólar baja frente al año anterior (−5.8 % en agosto y septiembre). La brecha llega a 10.9 puntos.

**5. Canasta por quintil (octubre 2026).**

| Quintil | Canasta (RD$) | Hace 12 meses (RD$) | Aumento | Veces el quintil 1 |
|---|---|---|---|---|
| Quintil 1 | 29,972.34 | 28,618.93 | +4.73 % | 1.00 |
| Quintil 2 | 39,120.01 | 37,262.10 | +4.99 % | 1.31 |
| Quintil 3 | 46,145.95 | 43,958.65 | +4.98 % | 1.54 |
| Quintil 4 | 53,389.75 | 50,925.40 | +4.84 % | 1.78 |
| Quintil 5 | 81,727.62 | 77,617.32 | +5.30 % | 2.73 |

**6. Agricultura, mayores alzas interanuales (minorista, octubre 2026).** Mango Gota de Oro +56.6 %, repollo +46.5 %, ajo criollo +39.8 %, guandul verde +34.4 % y yautía blanca +31.7 %. Raíces y tubérculos es el rubro con mayor alza promedio (12.79 %).

Los resultados cambian cada lunes, cuando el Job de Lakeflow actualiza las tablas Gold.
