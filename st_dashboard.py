import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="Citi Bike Strategy Dashboard",
    layout="wide"
)

st.title("Citi Bike Strategy Dashboard")
st.write("Interactive charts for Citi Bike trips and weather (2022).")

# ----------------------------
# Load required data
# ----------------------------
# Top 20 data (REQUIRED)
top20_path = "top20.csv"
if not os.path.exists(top20_path):
    st.error("❌ top20.csv not found. Put it in the same folder as st_dashboard.py")
    st.stop()

top20 = pd.read_csv(top20_path)

# ----------------------------
# Detect correct columns
# ----------------------------
# Trips column
possible_trip_cols = ["trips", "trip_count", "count", "value"]
trip_col = next((c for c in possible_trip_cols if c in top20.columns), None)

if trip_col is None:
    st.error("❌ Could not find a trips/count column in top20.csv")
    st.stop()

# Label column (station / route name)
label_col = next(
    (c for c in top20.columns if c != trip_col and top20[c].dtype == "object"),
    None
)

if label_col is None:
    st.error("❌ Could not find a label column in top20.csv")
    st.stop()

# ----------------------------
# Top 20 bar chart
# ----------------------------
st.subheader("Top 20 Stations / Routes by Trips")

top20_sorted = top20.sort_values(by=trip_col, ascending=False).head(20)

fig_bar = px.bar(
    top20_sorted,
    x=trip_col,
    y=label_col,
    orientation="h",
    title="Top 20 by Trips"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------
# Kepler.gl Map (REQUIRED)
# ----------------------------
st.subheader("Aggregated Bike Trips Map (Kepler.gl)")

html_file = "nyc_trips_kepler_map.html"
if not os.path.exists(html_file):
    st.error("❌ Kepler map HTML file not found. Export it and place it in this folder.")
    st.stop()

with open(html_file, "r", encoding="utf-8") as f:
    html_data = f.read()

st.components.v1.html(html_data, height=900, scrolling=True)