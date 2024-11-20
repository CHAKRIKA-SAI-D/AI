import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
hudco_dwelling = pd.read_csv("hudco_dwelling_approved_residential.csv")
road_quality = pd.read_csv("Table_4_1_a.csv")
materials_quality = pd.read_csv("Table_5_7.csv")
quality_control = pd.read_csv("Table_5_8.csv")

# Clean column names
hudco_dwelling.columns = hudco_dwelling.columns.str.strip().str.lower()
road_quality.columns = road_quality.columns.str.strip().str.lower()
materials_quality.columns = materials_quality.columns.str.strip().str.lower()
quality_control.columns = quality_control.columns.str.strip().str.lower()

# Display Data Previews
st.write("HUDCO Dwelling Data Preview:")
st.dataframe(hudco_dwelling.head())
st.write("Road Quality Data Preview:")
st.dataframe(road_quality.head())

# Display concise dataset summaries
st.write("HUDCO Dwelling Dataset Summary:")
st.dataframe(hudco_dwelling.isnull().sum().reset_index(name='Missing Values').rename(columns={'index': 'Column'}))

st.write("Road Quality Dataset Summary:")
st.dataframe(road_quality.isnull().sum().reset_index(name='Missing Values').rename(columns={'index': 'Column'}))

# Select and Visualize Metrics
# Choose metric for HUDCO Dwelling
st.sidebar.subheader("Select a Metric for HUDCO Dwelling")
hudco_columns = hudco_dwelling.select_dtypes(include=['float64', 'int64']).columns
metric_hudco = st.sidebar.selectbox("Select a Metric", hudco_columns)

# Visualization for HUDCO Dwelling
if metric_hudco:
    st.subheader(f"Visualization of {metric_hudco} by State")
    if 'state' in hudco_dwelling.columns:
        fig_hudco = px.bar(hudco_dwelling, x='state', y=metric_hudco, title=f"{metric_hudco} by State")
        st.plotly_chart(fig_hudco)

# Choose metric for Road Quality
st.sidebar.subheader("Select a Metric for Road Quality")
road_columns = road_quality.select_dtypes(include=['float64', 'int64']).columns
metric_road = st.sidebar.selectbox("Select a Metric", road_columns)

# Visualization for Road Quality
if metric_road:
    st.subheader(f"Visualization of {metric_road} by State")
    if 'state' in road_quality.columns:
        fig_road = px.bar(road_quality, x='state', y=metric_road, title=f"{metric_road} by State")
        st.plotly_chart(fig_road)

# Additional insights for Quality Control
st.sidebar.subheader("Select a Metric for Quality Control")
quality_columns = quality_control.select_dtypes(include=['float64', 'int64']).columns
metric_quality = st.sidebar.selectbox("Select a Metric", quality_columns)

# Visualization for Quality Control
if metric_quality:
    st.subheader(f"Visualization of {metric_quality}")
    if 'state' in quality_control.columns:
        fig_quality = px.bar(quality_control, x='state', y=metric_quality, title=f"{metric_quality} Insights")
        st.plotly_chart(fig_quality)

# Display messages
if not metric_hudco and not metric_road and not metric_quality:
    st.write("Please select a metric to visualize.")
