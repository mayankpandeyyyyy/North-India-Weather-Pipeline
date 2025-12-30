import streamlit as st
import pandas as pd
import os

# Set Page Config
st.set_page_config(page_title="North India Weather Portal", layout="wide")

# Navigation logic
if 'view' not in st.session_state:
    st.session_state.view = 'map'
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = None

def select_state(name):
    st.session_state.selected_state = name
    st.session_state.view = 'table'

def reset_to_home():
    st.session_state.view = 'map'
    st.session_state.selected_state = None

# Sidebar with your GitHub Link
with st.sidebar:
    st.title("Project Info")
    st.info("Developed by Mayank Pandey")
    st.markdown("[🔗 View GitHub Repository](https://github.com/mayankpandeyyyyy/North-India-Weather-Pipeline)")
    st.write("---")
    st.write("**Architecture:** Medallion (Bronze/Silver/Gold)")

if os.path.exists("gold_weather"):
    df = pd.read_parquet("gold_weather")
    
    # --- PAGE 1: STATE SELECTION VIEW ---
    if st.session_state.view == 'map':
        st.markdown("<h1 style='text-align: center;'>North India Weather Data</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Select a state to view local weather data</h3>", unsafe_allow_html=True)
        st.write("---")

        northern_states = ["Uttar Pradesh", "Punjab", "Haryana", "Himachal", "Uttarakhand"]
        
        cols = st.columns(len(northern_states))
        for i, state in enumerate(northern_states):
            with cols[i]:
                if st.button(state, use_container_width=True):
                    select_state(state)
        
        st.markdown("---")
        st.info("Select a state button above to see the processed data from the Gold Layer.")

    # --- PAGE 2: SEQUENTIAL TABLE VIEW ---
    elif st.session_state.view == 'table':
        state_name = st.session_state.selected_state
        
        if st.button("⬅ Back to Selection"):
            reset_to_home()
            st.rerun()
        
        st.title(f"Weather Report: {state_name}")
        
        # Filter and clean data
        state_df = df[df['State'] == state_name][['City', 'Temperature_C', 'Humidity', 'Wind_Speed_Kmph']]
        
        # Reset index to make it sequential starting from 1
        state_df = state_df.sort_values("Temperature_C", ascending=False).reset_index(drop=True)
        state_df.index = state_df.index + 1
        
        st.table(state_df)

else:
    st.error("Data source not found. Please run your pipeline scripts (01 to 03) first.")