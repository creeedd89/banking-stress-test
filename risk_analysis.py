import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

def load_data(filepath):
    return pd.read_csv(filepath, index_col=0, parse_dates=True)

def analyze_risk(df, event_date, bank, market_col='^GSPC', window=255, gap=10):
    """
    Analyzes systemic risk (Beta) decomposition before and after the event.
    """
    if event_date not in df.index:
        idx_options = df.index[df.index >= event_date]
        if len(idx_options) == 0:
            return None
        event_date = idx_options[0]
        
    event_idx = df.index.get_loc(event_date)
    
    # Pre-event window
    pre_end = event_idx - gap
    pre_start = pre_end - window
    
    # Post-event window
    post_start = event_idx + gap
    post_end = post_start + window
    
    if pre_start < 0 or post_end > len(df):
        # We don't have enough data on one of the ends
        return None
        
    df_pre = df.iloc[pre_start:pre_end].dropna(subset=[bank, market_col])
    df_post = df.iloc[post_start:post_end].dropna(subset=[bank, market_col])
    
    if len(df_pre) < window * 0.8 or len(df_post) < window * 0.8:
        return None
        
    # Helper function to calculate metrics
    def get_metrics(data):
        X = data[market_col]
        Y = data[bank]
        
        # Beta
        cov_matrix = np.cov(Y, X)
        cov_yx = cov_matrix[0, 1]
        var_x = cov_matrix[1, 1]
        beta = cov_yx / var_x
        
        # Correlation (Systemic Risk component)
        corr = np.corrcoef(Y, X)[0, 1]
        
        # Relative Volatility (Idiosyncratic component)
        rel_vol = Y.std() / X.std()
        
        return beta, corr, rel_vol
        
    pre_beta, pre_corr, pre_rel_vol = get_metrics(df_pre)
    post_beta, post_corr, post_rel_vol = get_metrics(df_post)
    
    return {
        'Beta_Pre': pre_beta,
        'Beta_Post': post_beta,
        'Beta_Change': post_beta - pre_beta,
        'Corr_Pre': pre_corr,
        'Corr_Post': post_corr,
        'Corr_Change': post_corr - pre_corr,
        'RelVol_Pre': pre_rel_vol,
        'RelVol_Post': post_rel_vol,
        'RelVol_Change': post_rel_vol - pre_rel_vol
    }

def run_risk_analysis(event_date_str, event_name, df=None, market_col='^GSPC', window=255, gap=10):
    if df is None:
        raise ValueError("DataFrame 'df' must be provided.")
        
    banks = [c for c in df.columns if c != market_col and 'Unnamed' not in c and c != 'Ticker']
    if df.empty:
        print("Dataframe is empty. Cannot run risk analysis.")
        return None
        
    event_date = pd.to_datetime(event_date_str)
    
    # We no longer check strict bounds here as fetch_data.py handles validation.
        
    results = []
    for bank in banks:
        metrics = analyze_risk(df, event_date, bank, market_col=market_col, window=window, gap=gap)
        if metrics:
            row = {'Event_Name': event_name, 'Event_Date': event_date_str, 'Bank': bank}
            row.update(metrics)
            results.append(row)
            
    if not results:
        print("No valid risk data found for this event across banks.")
        return None
        
    results_df = pd.DataFrame(results)
    results_df.to_csv('risk_results_raw.csv', index=False)
    
    # Summary Table
    summary = results_df[['Beta_Change', 'Corr_Change', 'RelVol_Change']].mean()
    print("\n--- Average Risk Changes ---")
    print(summary)
    
    return results_df
