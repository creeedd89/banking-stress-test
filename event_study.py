import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import os

def load_data(filepath):
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    return df

def calculate_car(df, event_date, bank, market_col='^GSPC', est_window=255, gap=10, event_window_start=-1, event_window_end=1):
    """
    Calculates the Cumulative Abnormal Return (CAR) for a specific event.
    """
    if event_date not in df.index:
        idx_options = df.index[df.index >= event_date]
        if len(idx_options) == 0:
            return None, None
        event_date = idx_options[0]
        
    event_idx = df.index.get_loc(event_date)
    
    est_end = event_idx - gap
    est_start = est_end - est_window
    
    if est_start < 0:
        return None, None
        
    evt_start = event_idx + event_window_start
    evt_end = event_idx + event_window_end + 1
    
    if evt_end > len(df):
        return None, None
        
    df_est = df.iloc[est_start:est_end].dropna(subset=[bank, market_col])
    df_evt = df.iloc[evt_start:evt_end].dropna(subset=[bank, market_col])
    
    if len(df_est) < (est_window * 0.8) or len(df_evt) == 0:
        return None, None

    X = sm.add_constant(df_est[market_col])
    Y = df_est[bank]
    model = sm.OLS(Y, X).fit()
    
    X_evt = sm.add_constant(df_evt[market_col])
    expected_returns = model.predict(X_evt)
    actual_returns = df_evt[bank]
    abnormal_returns = actual_returns - expected_returns
    
    car = abnormal_returns.sum()
    
    ar_est = Y - model.predict(X)
    ar_var = ar_est.var()
    
    N = len(df_evt)
    se_car = np.sqrt(N * ar_var)
    
    return car, se_car

def run_event_study(event_date_str, event_name, df=None, market_col='^GSPC', est_window=255, gap=10):
    if df is None:
        raise ValueError("DataFrame 'df' must be provided.")
        
    banks = [c for c in df.columns if c != market_col and 'Unnamed' not in c and c != 'Ticker']
    
    if df.empty:
        raise ValueError("Dataframe is empty. Cannot run event study.")
        
    event_date = pd.to_datetime(event_date_str)
    
    # We no longer check strict bounds here as fetch_data.py handles validation.
    # However, calculate_car still handles local bounds for the specific window.
        
    results = []
    for bank in banks:
        car, se_car = calculate_car(df, event_date, bank, market_col=market_col, est_window=est_window, gap=gap)
        if car is not None:
            t_stat = car / se_car if se_car != 0 else 0
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=est_window-2))
            
            results.append({
                'Event_Name': event_name,
                'Event_Date': event_date_str,
                'Bank': bank,
                'CAR': car,
                't-stat': t_stat,
                'p-value': p_value
            })
            
    if not results:
        print("No valid data found for this event across banks.")
        return None
        
    results_df = pd.DataFrame(results)
    results_df.to_csv('car_results_raw.csv', index=False)
    
    results_df['Significant'] = results_df['p-value'] < 0.05
    results_df['Positive'] = results_df['CAR'] > 0
    
    avg_car = results_df['CAR'].mean() * 100
    percent_positive = (results_df['Positive'].sum() / len(results_df)) * 100
    num_significant = results_df['Significant'].sum()
    
    print("\n--- Event Study Summary ---")
    print(f"Event: {event_name} ({event_date_str})")
    print(f"Average CAR: {avg_car:.2f}%")
    print(f"Percent Positive: {percent_positive:.1f}%")
    print(f"Significant Reactions: {num_significant} out of {len(results_df)} banks")
    
    return results_df
