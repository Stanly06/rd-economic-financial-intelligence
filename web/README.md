# Web platform (ES / EN)

Live: **https://stanly06.github.io/rd-intelligence/** (Spanish: `?lang=es`, English: `?lang=en`)

A single-file, bilingual web version of the platform. Every number comes from the Gold (and a few Silver) tables; nothing is simulated.

| File | Role |
|---|---|
| `shell.html` | Page skeleton (header, sidebar, language switch, theme) |
| `styles.css` | Styles (light "Dominicana Institucional" and dark "Financial Intelligence" themes) |
| `app.js` | Pages, filters, KPI cards, charts (Chart.js), detail tables and ES/EN texts |
| `build.py` | Embeds the data export into one HTML file |

Pages: economic overview, inflation & CPI, exchange rate (since 1991), family basket, fuel, consumer prices, electricity, agricultural prices (product groups, products, market comparison AGR-007), sources & methodology.

## Refresh

1. Run [`src/exports/08_Web_Platform_Export`](../src/exports/08_Web_Platform_Export.ipynb) in Databricks (writes `gold/web_exports/rd_platform_data.json`).
2. `databricks fs cp dbfs:/Volumes/rd_economic_intelligence/gold/web_exports/rd_platform_data.json data.json`
3. `python web/build.py data.json index.html` and publish `index.html` to the portfolio site (`rd-intelligence/index.html`).

Only aggregated, published statistics are exported; source files are never published.
