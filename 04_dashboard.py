import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="North India Weather Intelligence", layout="wide")

if os.path.exists("gold_weather"):
    df = pd.read_parquet("gold_weather")

    # --- FEATURE ENGINEERING ---
    # Calculating Logistics Risk and Energy Load on the fly
    def analyze_impact(row):
        if row['Humidity'] > 80 and row['Temperature_C'] < 12:
            return "⚠️ High Fog Risk (Transport Delay)"
        elif row['Temperature_C'] > 30:
            return "⚡ High Cooling Demand"
        elif row['Temperature_C'] < 8:
            return "🔥 High Heating Demand"
        else:
            return "✅ Optimal Conditions"

    df['Business_Impact'] = df.apply(analyze_impact, axis=1)

    st.title("🏙️ North India Weather Intelligence Engine")
    st.markdown("### Translating Real-time Meteorological Data into Actionable Business Insights")

    # --- KPI ROW ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Cities Monitored", len(df))
    kpi2.metric("Avg Regional Temp", f"{round(df['Temperature_C'].mean(), 1)}°C")
    kpi3.metric("Critical Alerts", len(df[df['Business_Impact'].str.contains("⚠️")]))
    kpi4.metric("Data Pipeline Status", "Stable")

    st.divider()

    # --- INTERACTIVE ANALYTICS ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Comparison Filters")
        selected_states = st.multiselect("Select States:", df['State'].unique(), default=df['State'].unique())
        selected_impact = st.multiselect("Impact Category:", df['Business_Impact'].unique(), default=df['Business_Impact'].unique())
        
        filtered_df = df[(df['State'].isin(selected_states)) & (df['Business_Impact'].isin(selected_impact))]
        
        st.write(f"Showing **{len(filtered_df)}** results")
        st.dataframe(filtered_df[['City', 'Temperature_C', 'Business_Impact']], use_container_width=True, hide_index=True)

    with col2:
        st.subheader("State-wise Temperature & Humidity Distribution")
        # Scatter plot to show clusters
        fig = px.scatter(filtered_df, x="Temperature_C", y="Humidity", color="State", 
                         size="Wind_Speed_Kmph", hover_name="City",
                         title="Climatic Clustering (Size = Wind Speed)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- REGIONAL RISK BAR CHART ---
    st.subheader("Regional Logistics & Energy Risk Profile")
    fig_bar = px.bar(filtered_df, x="State", color="Business_Impact", 
                     title="Business Impact Events by State", barmode='group')
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Gold Data not found. Run orchestrator.py first.")