import os
from config import REGIONS, HISTORICAL_EVENTS
from fetch_data import fetch_data_for_region
from event_study import run_event_study
from risk_analysis import run_risk_analysis
from generate_report import generate_reports

def print_menu(title, options_dict, display_key="name"):
    print(f"\n--- {title} ---")
    for key, value in options_dict.items():
        print(f"{key}. {value[display_key]}")
        
def get_user_choice(options_dict, prompt="Select an option: "):
    while True:
        choice = input(prompt)
        if choice in options_dict:
            return choice
        print("Invalid choice, please try again.")

def main():
    print("🌍 Welcome to the Global Interactive Event Study Analyzer 🌍")
    
    # 1. Select Region
    print_menu("Select Region / Stock Market", REGIONS)
    region_choice = get_user_choice(REGIONS)
    region_data = REGIONS[region_choice]
    
    if region_data["name"] == "Custom Input":
        market_index = input("Enter Market Index ticker (e.g., ^GSPC): ")
        banks_input = input("Enter Bank tickers separated by comma (e.g., JPM,BAC,C): ")
        bank_tickers = [b.strip() for b in banks_input.split(',')]
        region_name = "Custom Region"
    else:
        market_index = region_data["index"]
        bank_tickers = region_data["banks"]
        region_name = region_data["name"]
        
    print(f"\nSelected: {region_name} | Index: {market_index} | Banks: {', '.join(bank_tickers)}")
    
    # 2. Select Event
    print_menu("Select Historical Event", HISTORICAL_EVENTS)
    event_choice = get_user_choice(HISTORICAL_EVENTS)
    event_data = HISTORICAL_EVENTS[event_choice]
    
    if event_data["name"] == "Custom Date":
        event_name = input("Enter a name for this custom event: ")
        event_date_str = input("Enter the event date (YYYY-MM-DD): ")
    else:
        event_name = event_data["name"]
        event_date_str = event_data["date"]
        
    print(f"\nSelected Event: {event_name} on {event_date_str}")
    
    # 3. Select Parameters
    try:
        est_window = int(input("\nEnter Estimation Window in days (default 255): ") or 255)
        gap = int(input("Enter Gap between estimation and event in days (default 10): ") or 10)
    except ValueError:
        print("Invalid input, defaulting to 255 and 10.")
        est_window = 255
        gap = 10
        
    print("\n🚀 Starting Analysis Pipeline...")
    
    # Step 1: Fetch Data
    print("\n[1/4] Fetching Data...")
    # Fetch from 1999 to ensure we have data for older events
    success = fetch_data_for_region(market_index, bank_tickers, start_date="1999-01-01")
    if not success:
        print("Pipeline aborted due to data fetch failure.")
        return
        
    # Step 2: Event Study
    print("\n[2/4] Running Event Study (CAR)...")
    car_df = run_event_study(event_date_str, event_name, market_col=market_index, est_window=est_window, gap=gap)
    
    # Step 3: Risk Analysis
    print("\n[3/4] Running Risk Analysis (Beta & Correlation)...")
    risk_df = run_risk_analysis(event_date_str, event_name, market_col=market_index, window=est_window, gap=gap)
    
    # Step 4: Generate Reports
    print("\n[4/4] Generating Reports and Visualizations...")
    generate_reports(event_name)
    
    print("\n✅ Pipeline Complete! Check 'car_boxplot.png' and 'risk_change_barplot.png' for the visualizations.")

if __name__ == "__main__":
    main()
