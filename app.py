import streamlit as st
import pandas as pd
from config import CONTINENTS
from fetch_data import fetch_data_for_region
from event_study import run_event_study
from risk_analysis import run_risk_analysis
from generate_report import generate_reports

st.set_page_config(page_title="Global Event Study Analyzer", page_icon="🌍", layout="wide")

st.title("🌍 Global Market Event & Stress Test Analyzer")
st.markdown("""
Analyze the quantitative impact of major historical events—from natural disasters and terrorist attacks to financial frauds and political shocks—across global stock markets.
""")

# --- Sidebar Configuration ---
st.sidebar.header("1. Select Geography")

# Continent Selection
continents = list(CONTINENTS.keys())
selected_continent = st.sidebar.selectbox("Select Continent", continents)

# Country Selection
countries = list(CONTINENTS[selected_continent].keys())
selected_country = st.sidebar.selectbox("Select Country / Stock Market", countries)

country_data = CONTINENTS[selected_continent][selected_country]
market_index = country_data["index"]
banks = country_data["banks"]

st.sidebar.markdown(f"**Market Index:** `{market_index}`")
st.sidebar.markdown(f"**Tracked Banks:** `{', '.join(banks)}`")

# --- Event Selection ---
st.sidebar.header("2. Select Historical Event")

events = country_data["events"]
event_names = [f"{e['name']} ({e['date']}) - {e['category']}" for e in events]
selected_event_str = st.sidebar.selectbox("Select Event", event_names)

# Extract just the name for our functions
selected_event_name = selected_event_str.split(" (")[0]
selected_event_date = [e['date'] for e in events if e['name'] == selected_event_name][0]

# --- Parameters ---
st.sidebar.header("3. Analysis Parameters")
est_window = st.sidebar.number_input("Estimation Window (days)", min_value=30, max_value=500, value=255)
gap = st.sidebar.number_input("Gap (days)", min_value=0, max_value=50, value=10)

# --- Main Action ---
run_btn = st.sidebar.button("🚀 Run Analysis", type="primary")

if run_btn:
    if market_index == "ICE":
        st.error("🐧 **Error:** The Penguin Exchange (ICE) is currently frozen. Trading is suspended until the Great Ice Melt. Please select a valid country!")
    else:
        with st.status("Running Quantitative Pipeline...", expanded=True) as status:
            st.write(f"Fetching data for {selected_country} from 1980...")
            success = fetch_data_for_region(market_index, banks, start_date="1980-01-01")
            
            if not success:
                status.update(label="Data Fetch Failed", state="error")
                st.error("Failed to fetch historical market data from Yahoo Finance. This may happen if tickers were delisted.")
            else:
                st.write("Computing Cumulative Abnormal Returns (CAR)...")
                car_df = run_event_study(selected_event_date, selected_event_name, market_col=market_index, est_window=est_window, gap=gap)
                
                st.write("Decomposing Systematic (Beta) and Systemic Risk...")
                risk_df = run_risk_analysis(selected_event_date, selected_event_name, market_col=market_index, window=est_window, gap=gap)
                
                if car_df is None or risk_df is None:
                    status.update(label="Insufficient Data", state="error")
                    st.error(f"Not enough historical data available around the event date ({selected_event_date}) for this market.")
                else:
                    st.write("Rendering visualizations...")
                    fig_car, fig_risk = generate_reports(selected_event_name)
                    
                    status.update(label="Analysis Complete!", state="complete")
                    
                    st.success("Pipeline executed successfully!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Market Reaction (CAR)")
                        if fig_car:
                            st.pyplot(fig_car)
                        st.dataframe(car_df[['Bank', 'CAR', 'p-value', 'Significant']])
                        
                    with col2:
                        st.subheader("Risk Dynamics")
                        if fig_risk:
                            st.pyplot(fig_risk)
                        st.dataframe(risk_df[['Bank', 'Beta_Change', 'Corr_Change']])
