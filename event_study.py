import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import os

def load_data(filepath):
    # Simply read the CSV. 
    # With our fetch_data.py, it's a single header row of tickers.
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    return df

def calculate_car(df, event_date, bank, market_col='^GSPC', est_window=255, gap=10, event_window_start=-1, event_window_end=1):
    """
    Calculates the Cumulative Abnormal Return (CAR) for a specific event.
    """
    # Find the integer index of the event date
    # If exact date is not a trading day, find the next available one
    if event_date not in df.index:
        idx_options = df.index[df.index >= event_date]
        if len(idx_options) == 0:
            return None, None
        event_date = idx_options[0]
        
    event_idx = df.index.get_loc(event_date)
    
    # Estimation window indices
    est_end = event_idx - gap
    est_start = est_end - est_window
    
    if est_start < 0:
        print(f"Not enough data for estimation window for event {event_date.date()}")
        return None, None
        
    # Event window indices
    evt_start = event_idx + event_window_start
    evt_end = event_idx + event_window_end + 1 # +1 because python slices are exclusive
    
    # Data slices
    df_est = df.iloc[est_start:est_end].dropna(subset=[bank, market_col])
    df_evt = df.iloc[evt_start:evt_end].dropna(subset=[bank, market_col])
    
    if len(df_est) < (est_window * 0.8) or len(df_evt) == 0:
        return None, None

    # OLS Regression for estimation window
    X = sm.add_constant(df_est[market_col])
    Y = df_est[bank]
    model = sm.OLS(Y, X).fit()
    alpha, beta = model.params
    
    # Calculate AR in the event window
    X_evt = sm.add_constant(df_evt[market_col])
    expected_returns = model.predict(X_evt)
    actual_returns = df_evt[bank]
    abnormal_returns = actual_returns - expected_returns
    
    # CAR
    car = abnormal_returns.sum()
    
    # Variance of AR in estimation window (for significance testing)
    ar_est = Y - model.predict(X)
    ar_var = ar_est.var()
    
    # Standard error of CAR = sqrt(N * variance) 
    # (assuming independence, ignoring small adjustment factor for prediction)
    N = len(df_evt)
    se_car = np.sqrt(N * ar_var)
    
    return car, se_car

def main():
    filepath = 'bank_returns.csv'
    if not os.path.exists(filepath):
        print("Data file not found.")
        return
        
    df = load_data(filepath)
    print("Data loaded successfully.")
    print("Available columns:", df.columns.tolist())
    
    market = '^GSPC'
    banks = [c for c in df.columns if c != market and 'Unnamed' not in c and c != 'Ticker']
    
    # Federal Reserve Stress Test Result Dates
    events = [
        "2019-06-27",
        "2020-06-25",
        "2021-06-24",
        "2022-06-23",
        "2023-06-28",
        "2024-06-26",
        "2025-06-27",
        "2026-06-24"
    ]
    
    results = []
    
    for event_str in events:
        event_date = pd.to_datetime(event_str)
        # Check if event is within our data range
        if event_date > df.index[-1] or event_date < df.index[0]:
            print(f"Skipping {event_str}, out of data bounds.")
            continue
            
        for bank in banks:
            car, se_car = calculate_car(df, event_date, bank, market_col=market)
            if car is not None:
                t_stat = car / se_car if se_car != 0 else 0
                p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=255-2)) # two-tailed
                
                results.append({
                    'Event_Year': event_date.year,
                    'Event_Date': event_str,
                    'Bank': bank,
                    'CAR': car,
                    't-stat': t_stat,
                    'p-value': p_value
                })
                
    results_df = pd.DataFrame(results)
    
    # Save raw results
    results_df.to_csv('car_results_raw.csv', index=False)
    
    # Calculate average CARs per event year
    avg_cars = results_df.groupby('Event_Year')['CAR'].mean() * 100 # In percentage
    print("\n--- Average CARs by Event Year (%) ---")
    print(avg_cars)
    
    # Summarize significance
    # Count how many banks had a significant reaction at 5% level
    results_df['Significant'] = results_df['p-value'] < 0.05
    results_df['Positive'] = results_df['CAR'] > 0
    
    summary = results_df.groupby('Event_Year').agg(
        Total_Banks=('Bank', 'count'),
        Avg_CAR=('CAR', lambda x: x.mean() * 100),
        Percent_Positive=('Positive', lambda x: (x.sum() / len(x)) * 100),
        Num_Significant=('Significant', 'sum')
    )
    
    print("\n--- Summary by Event Year ---")
    print(summary)
    
if __name__ == "__main__":
    main()
