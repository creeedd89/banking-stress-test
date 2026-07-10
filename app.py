import streamlit as st
import pandas as pd
import yaml
import plotly.express as px

from fetch_data import fetch_data_for_region
from event_study import run_event_study
from risk_analysis import run_risk_analysis
from generate_report import generate_reports
from data_sources.fallback import DataUnavailableError

with open('markets.yaml', 'r', encoding='utf-8') as f:
    CONTINENTS = yaml.safe_load(f)

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
market_index = country_data.get("index_ticker", "")
banks_dict = country_data.get("banks", {})
banks = list(banks_dict.values())

st.sidebar.markdown(f"**Market Index:** `{market_index}`")
if banks:
    st.sidebar.markdown(f"**Tracked Banks:** `{', '.join(banks)}`")
else:
    st.sidebar.markdown(f"**Tracked Banks:** `None`")

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

st.sidebar.header("4. Upload Custom Data")
st.sidebar.markdown("Upload missing bank data as a CSV. Filename must match the ticker (e.g., `JPM.csv`). The CSV must contain `Date` and `Close` columns.")
uploaded_files = st.sidebar.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    import os
    os.makedirs(os.path.join("data", "cache"), exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = os.path.join("data", "cache", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"Saved {len(uploaded_files)} file(s) for local access!")

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
    showcountries=True, countrycolor="white",
    showcoastlines=True, coastlinecolor="white",
    showland=True, landcolor="#55a630",
    showocean=True, oceancolor="#0077b6",
    projection_rotation=dict(lon=lon, lat=lat, roll=0),
    bgcolor="rgba(0,0,0,0)"
)
fig_globe.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
fig_globe.update_traces(marker=dict(color="#FF4B4B", size=15))

st.plotly_chart(fig_globe)

# --- Main Action ---
run_btn = st.sidebar.button("🚀 Run Analysis", type="primary")

if st.sidebar.button("🗑️ Clear Cache & Re-fetch"):
    st.cache_data.clear()
    st.sidebar.success("Cache cleared! Next run will fetch fresh data.")

if run_btn:
    if market_index == "ICE":
        st.error("🐧 **Error:** The Penguin Exchange (ICE) is currently frozen. Trading is suspended until the Great Ice Melt. Please select a valid country!")
    else:
        with st.status("Running Quantitative Pipeline...", expanded=True) as status:
            st.write(f"Fetching data for {selected_country} from 1980...")
            try:
                # Fetch data and get the DataFrame directly
                returns_df = fetch_data_for_region(
                    selected_country, 
                    market_index, 
                    banks, 
                    start_date="1980-01-01", 
                    min_rows=est_window+gap,
                    event_date=selected_event_date
                )
                
                st.write("Computing Cumulative Abnormal Returns (CAR)...")
                car_df = run_event_study(selected_event_date, selected_event_name, df=returns_df, market_col=market_index, est_window=est_window, gap=gap)
                
                st.write("Decomposing Systematic (Beta) and Systemic Risk...")
                risk_df = run_risk_analysis(selected_event_date, selected_event_name, df=returns_df, market_col=market_index, window=est_window, gap=gap)
                
                if car_df is None or risk_df is None:
                    status.update(label="Insufficient Data", state="error")
                    st.error(f"Not enough historical data available around the event date ({selected_event_date}) for this market.")
                else:
                    st.write("Rendering visualizations...")
                    fig_car, fig_risk = generate_reports(selected_event_name)
                    
                    status.update(label="Analysis Complete!", state="complete")
                    
                    st.success("Pipeline executed successfully!")
                    
                    # Add Top-Level Metrics
                    st.markdown("### 📊 Event Impact Summary")
                    metrics_cols = st.columns(3)
                    
                    avg_car = car_df['CAR'].mean() * 100
                    sig_banks = car_df['Significant'].sum()
                    avg_beta_change = risk_df['Beta_Change'].mean()
                    
                    metrics_cols[0].metric("Average CAR", f"{avg_car:.2f}%", delta=f"{avg_car:.2f}%")
                    metrics_cols[1].metric("Significant Bank Reactions", f"{sig_banks} / {len(car_df)}")
                    metrics_cols[2].metric("Avg Systemic Risk (Beta) Shift", f"{avg_beta_change:.2f}")
                    
                    st.divider()
                    
                    tab1, tab2, tab3 = st.tabs(["📉 Market Reaction (CAR)", "🌪️ Risk Dynamics", "💾 Export Data"])
                    
                    with tab1:
                        if fig_car:
                            st.pyplot(fig_car)
                        st.dataframe(car_df[['Bank', 'CAR', 'p-value', 'Significant']])
                        
                    with tab2:
                        if fig_risk:
                            st.pyplot(fig_risk)
                        st.dataframe(risk_df[['Bank', 'Beta_Change', 'Corr_Change']])

                    with tab3:
                        st.markdown("Download the raw analysis results for further inspection:")
                        st.download_button("Download CAR Data (CSV)", data=car_df.to_csv(index=False), file_name="car_results.csv", mime="text/csv")
                        st.download_button("Download Risk Data (CSV)", data=risk_df.to_csv(index=False), file_name="risk_results.csv", mime="text/csv")

                    st.balloons()
            except DataUnavailableError as e:
                status.update(label="Data Fetch Failed", state="error")
                st.error(f"**Data Unavailable:** {e.message}")
                st.warning(f"**Failed Ticker:** `{e.ticker}`\n\n**Sources Attempted:** {', '.join(e.sources_tried)}\n\n*Suggestion: Try a shorter estimation window or add a local CSV file in `data/cache/{e.ticker.replace('^', '').replace('.', '_')}.csv`.*")
            except Exception as e:
                status.update(label="Analysis Error", state="error")
                st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    from streamlit.runtime import exists
    if not exists():
        import sys
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

# Trigger Streamlit Reload
