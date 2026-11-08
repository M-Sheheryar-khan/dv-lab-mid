import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Life Expectancy Dashboard", layout="wide")

# Load the cleaned data from Part 1
df = pd.read_csv(Path(__file__).parent.parent / "data" / "clean" / "wdi_clean.csv")

# Metric choices: label shown to the user -> column in the data
METRICS = {
    "Life expectancy (years)": "life_expectancy",
    "GDP per capita (US$)": "gdp_per_capita",
    "CO2 per capita (tonnes)": "co2_per_capita",
    "Internet users (% of population)": "internet_users_pct",
}

# ---------- Sidebar controls ----------
st.sidebar.header("Filters")
year = st.sidebar.slider("Year", int(df["year"].min()), int(df["year"].max()), 2022)
all_regions = sorted(df["region"].unique())
regions = st.sidebar.multiselect("Regions", all_regions, default=all_regions)
metric_label = st.sidebar.selectbox("Measure (map and rankings)", list(METRICS))
metric = METRICS[metric_label]

# Data for the chosen year and regions
data = df[(df["year"] == year) & (df["region"].isin(regions))].dropna(subset=[metric])
if data.empty:
    st.warning("No data for this selection. Pick at least one region.")
    st.stop()

# ---------- Title and summary numbers ----------
st.title("Life Expectancy, Income and Region")
st.caption("Source: World Bank WDI (CC BY 4.0). Use the sidebar to change year, regions and measure.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Countries shown", len(data))
c2.metric(f"Average ({year})", f"{data[metric].mean():,.1f}")
best = data.loc[data[metric].idxmax()]
worst = data.loc[data[metric].idxmin()]
c3.metric("Highest", best["country"], f"{best[metric]:,.1f}", delta_color="off")
c4.metric("Lowest", worst["country"], f"{worst[metric]:,.1f}", delta_color="off")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Rankings", "Data"])

with tab1:
    left, right = st.columns(2)
    # Income vs life expectancy, bubble area = population
    fig = px.scatter(data, x="gdp_per_capita", y="life_expectancy", size="population",
                     color="region", hover_name="country", log_x=True, size_max=40,
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     labels={"gdp_per_capita": "GDP per capita (US$, log scale)",
                             "life_expectancy": "Life expectancy (years)", "region": "Region"},
                     title="Richer countries live longer")
    left.plotly_chart(fig, use_container_width=True)
    # Map of the chosen measure
    fig = px.choropleth(data, locations="iso3", color=metric, hover_name="country",
                        color_continuous_scale="Blues", labels={metric: metric_label},
                        title=metric_label + " by country")
    fig.update_geos(projection_type="natural earth", showframe=False)
    right.plotly_chart(fig, use_container_width=True)

with tab2:
    # Average of the chosen measure per region over all years, with the selected year marked
    trend = (df[df["region"].isin(regions)].groupby(["year", "region"])[metric]
             .mean().reset_index())
    fig = px.line(trend, x="year", y=metric, color="region",
                  color_discrete_sequence=px.colors.qualitative.Safe,
                  labels={metric: metric_label, "year": "Year", "region": "Region"},
                  title=metric_label + " over time, by region")
    fig.add_vline(x=year, line_dash="dash", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    left, right = st.columns(2)
    top = data.nlargest(10, metric).sort_values(metric)
    bottom = data.nsmallest(10, metric).sort_values(metric, ascending=False)
    fig = px.bar(top, x=metric, y="country", orientation="h", color_discrete_sequence=["#08519c"],
                 labels={metric: metric_label, "country": ""}, title="Top 10")
    left.plotly_chart(fig, use_container_width=True)
    fig = px.bar(bottom, x=metric, y="country", orientation="h", color_discrete_sequence=["#6baed6"],
                 labels={metric: metric_label, "country": ""}, title="Bottom 10")
    right.plotly_chart(fig, use_container_width=True)

with tab4:
    st.write(f"{len(data)} countries, {year}")
    table = data[["country", "region", "life_expectancy", "gdp_per_capita",
                  "co2_per_capita", "internet_users_pct", "population"]]
    st.dataframe(table.sort_values("country"), use_container_width=True, hide_index=True)
    st.download_button("Download this table as CSV", table.to_csv(index=False), f"data_{year}.csv")
