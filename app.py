import streamlit as st
import pandas as pd
from config import CONTINENTS
from fetch_data import fetch_data_for_region
from event_study import run_event_study
from risk_analysis import run_risk_analysis
from generate_report import generate_reports
import plotly.express as px

COUNTRY_COORDS = {
    "United States": (38, -97), "Canada": (60, -95), "Mexico": (23, -102),
    "Brazil": (-14, -51), "Argentina": (-38, -63), "Chile": (-35, -71),
    "Colombia": (4, -72), "Peru": (-9, -75), "Venezuela": (8, -66),
    "United Kingdom": (55, -3), "Germany": (51, 9), "France": (46, 2),
    "Italy": (41, 12), "Spain": (40, -4), "Netherlands": (52, 5),
    "Switzerland": (47, 8), "Sweden": (60, 15), "Norway": (60, 8),
    "Greece": (39, 22), "Portugal": (39, -8), "Ireland": (53, -8),
    "Poland": (52, 20), "Turkey": (39, 35), "Russia": (60, 90),
    "Ukraine": (48, 30), "Israel": (31, 35), "Saudi Arabia": (25, 45),
    "United Arab Emirates": (23, 54), "Qatar": (25, 51), "Lebanon": (33, 35),
    "Iran": (32, 53), "Iraq": (33, 44), "Jordan": (31, 36),
    "Kuwait": (29, 47), "Bahrain": (26, 50), "Oman": (21, 57),
    "Egypt": (26, 30), "South Africa": (-30, 25), "Nigeria": (10, 8),
    "Kenya": (1, 38), "Morocco": (32, -5), "Tunisia": (34, 9),
    "Senegal": (14, -14), "Ghana": (8, -1), "Algeria": (28, 1),
    "Ethiopia": (9, 40), "India": (20, 77), "Pakistan": (30, 70),
    "Bangladesh": (24, 90), "Sri Lanka": (7, 81), "China": (35, 105),
    "Japan": (36, 138), "South Korea": (36, 127), "Taiwan": (23, 121),
    "Hong Kong": (22, 114), "Singapore": (1, 103), "Indonesia": (-5, 120),
    "Thailand": (15, 100), "Vietnam": (14, 108), "Malaysia": (4, 109),
    "Philippines": (13, 122), "Australia": (-25, 133), "New Zealand": (-40, 174)
}

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
selected_index = event_names.index(selected_event_str)
selected_event = events[selected_index]
selected_event_name = selected_event['name']
selected_event_date = selected_event['date']

# --- Parameters ---
st.sidebar.header("3. Analysis Parameters")
est_window = st.sidebar.number_input("Estimation Window (days)", min_value=30, max_value=500, value=255)
gap = st.sidebar.number_input("Gap (days)", min_value=0, max_value=50, value=10)

# --- Interactive Globe ---
lat, lon = COUNTRY_COORDS.get(selected_country, (0, 0))

df_map = pd.DataFrame({
    "Country": [selected_country],
    "Lat": [lat],
    "Lon": [lon],
    "Size": [1]
})

fig_globe = px.scatter_geo(
    df_map, lat="Lat", lon="Lon", hover_name="Country", size="Size",
    projection="orthographic"
)
fig_globe.update_geos(
    showcountries=True, countrycolor="#444444",
    showcoastlines=True, coastlinecolor="#444444",
    showland=True, landcolor="rgba(30, 30, 30, 1.0)",
    showocean=True, oceancolor="rgba(10, 10, 10, 1.0)",
    projection_rotation=dict(lon=lon, lat=lat, roll=0),
    bgcolor="rgba(0,0,0,0)"
)
fig_globe.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
fig_globe.update_traces(marker=dict(color="#FF4B4B", size=15))

st.plotly_chart(fig_globe, use_container_width=True)

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

if __name__ == "__main__":
    from streamlit.runtime import exists
    if not exists():
        import sys
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
