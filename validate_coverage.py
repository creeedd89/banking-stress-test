import config

def validate_coverage():
    continents = config.CONTINENTS
    
    total_events_global = 0
    total_countries = 0
    
    print("==========================================")
    print("🌍 GLOBAL EVENT COVERAGE VALIDATION REPORT")
    print("==========================================\n")
    
    missing_data_flags = []

    for continent, countries in continents.items():
        print(f"--- {continent} ---")
        continent_events = 0
        
        for country, data in countries.items():
            total_countries += 1
            index = data.get("index", "")
            banks = data.get("banks", [])
            events = data.get("events", [])
            
            event_count = len(events)
            continent_events += event_count
            total_events_global += event_count
            
            print(f"  {country}: {event_count} events")
            
            # Validation Checks
            if event_count == 0:
                missing_data_flags.append(f"[WARNING] {country} has 0 events!")
            
            if "TODO" in index:
                missing_data_flags.append(f"[TODO] {country} is missing a valid Market Index ({index})")
                
            for b in banks:
                if "TODO" in b:
                    missing_data_flags.append(f"[TODO] {country} is missing valid Bank Tickers ({b})")

        print(f"  -> Total for {continent}: {continent_events} events\n")
        
    print("==========================================")
    print(f"Total Continents: {len(continents)}")
    print(f"Total Countries Covered: {total_countries}")
    print(f"Total Historical Events: {total_events_global}")
    print("==========================================\n")
    
    if missing_data_flags:
        print("🚨 ACTION REQUIRED (MISSING YFINANCE DATA):")
        for flag in missing_data_flags:
            print(f"  - {flag}")
    else:
        print("✅ ALL SYSTEMS GO: No missing data or zero-event countries flagged.")

if __name__ == "__main__":
    validate_coverage()
