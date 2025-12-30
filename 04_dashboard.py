import streamlit as st
import pandas as pd
import os

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

if os.path.exists("gold_weather"):
    # Load and clean data
    df = pd.read_parquet("gold_weather")
    
    # --- PAGE 1: STATE SELECTION VIEW ---
    if st.session_state.view == 'map':
        st.markdown("<h1 style='text-align: center;'>North India Weather Data</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Select a state to view local weather data</h3>", unsafe_allow_html=True)
        st.write("---")

        # States list (Rajasthan removed as requested)
        northern_states = ["Uttar Pradesh", "Punjab", "Haryana", "Himachal", "Uttarakhand"]
        
        # Create a clean grid of "Click Options"
        cols = st.columns(len(northern_states))
        for i, state in enumerate(northern_states):
            with cols[i]:
                if st.button(state, use_container_width=True):
                    select_state(state)
        
        st.markdown("---")
        st.info(" Double click on any state button above to see the detailed meteorological report.")

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
        
        st.subheader("Current Observations")
        st.table(state_df)

else:
    st.error("Data source not found. Please run orchestrator.py.")