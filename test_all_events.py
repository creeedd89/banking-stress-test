import config
from fetch_data import fetch_data_for_region
from event_study import run_event_study
import pandas as pd
import sys

def run_tests():
    continents = config.CONTINENTS
    
    total_events = 0
    passed = 0
    failed = []
    
    print("==========================================")
    print("🚀 AUTOMATED PIPELINE TEST RUNNER")
    print("==========================================\n")
    
    for continent, countries in continents.items():
        for country, data in countries.items():
            market_index = data.get("index", "")
            banks = data.get("banks", [])
            events = data.get("events", [])
            
            if "TODO" in market_index:
                print(f"Skipping {country}: Missing Market Index ({market_index})")
                continue
                
            valid_banks = [b for b in banks if "TODO" not in b]
            if not valid_banks:
                print(f"Skipping {country}: Missing Bank Tickers")
                continue
            
            print(f"\n--- Testing {country} ({market_index}) ---")
            
            # Fetch data once per country from 1980 just like app.py
            success = fetch_data_for_region(market_index, valid_banks, start_date="1980-01-01")
            
            if not success:
                print(f"❌ DATA FETCH FAILED for {country}")
                for e in events:
                    total_events += 1
                    failed.append((country, e['name'], e['date'], "Fetch Failed"))
                continue
                
            for e in events:
                total_events += 1
                event_name = e['name']
                event_date = e['date']
                
                print(f"  Testing Event: {event_name} ({event_date})")
                
                try:
                    # est_window=255, gap=10 (defaults in app.py)
                    car_df = run_event_study(event_date, event_name, market_col=market_index, est_window=255, gap=10)
                    
                    if car_df is None:
                        print(f"    ❌ FAILED: Insufficient Data around {event_date}")
                        failed.append((country, event_name, event_date, "Insufficient Data for Event Study"))
                    else:
                        print(f"    ✅ PASSED")
                        passed += 1
                except Exception as ex:
                    print(f"    ❌ CRASH: {ex}")
                    failed.append((country, event_name, event_date, f"Crash: {ex}"))
                    
    print("\n==========================================")
    print("📊 TEST SUMMARY")
    print("==========================================")
    print(f"Total Events Tested: {total_events}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(failed)}")
    print("==========================================\n")
    
    if failed:
        print("🚨 FAILURE LOG:")
        for f in failed:
            print(f"  - {f[0]}: {f[1]} ({f[2]}) -> {f[3]}")
            
if __name__ == "__main__":
    run_tests()
