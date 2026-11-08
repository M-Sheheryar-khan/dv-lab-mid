# Life Expectancy, Income and Region: Dashboard

Live dashboard: https://dv-lab-mid-jiltjzqgdskifmnp6pznju.streamlit.app/

Interactive dashboard for the DSC 327 mid lab project (BDS 6, COMSATS University Islamabad).

## What it shows
- Summary numbers: countries shown, average, highest and lowest.
- Overview tab: income vs life expectancy (bubble area = population) and a world map.
- Trends tab: change over time by region.
- Rankings tab: top 10 and bottom 10 countries.
- Data tab: sortable table with CSV download.
- Sidebar controls: year, regions, and measure. Hover for exact values.

## Data
World Bank World Development Indicators (WDI), CC BY 4.0. Cleaning decisions are in cleaning_log.md. Cleaned file: data/clean/wdi_clean.csv.

## How to run locally
    pip install streamlit pandas plotly
    streamlit run dashboard/app.py

## Files
- notebook.ipynb: full analysis, Parts 1 to 9
- figures/: exported charts
- dashboard/app.py: the dashboard
- cleaning_log.md: every cleaning decision