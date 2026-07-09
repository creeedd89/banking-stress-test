import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    sns.set_theme(style="whitegrid")
    
    # 1. Plot CARs
    if os.path.exists('car_results_raw.csv'):
        car_df = pd.read_csv('car_results_raw.csv')
        # Convert CAR to percentage
        car_df['CAR (%)'] = car_df['CAR'] * 100
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=car_df, x='Event_Year', y='CAR (%)', hue='Event_Year', palette="vlag", legend=False)
        plt.title('Cumulative Abnormal Returns (CAR) by Stress Test Year', fontsize=14)
        plt.axhline(0, color='black', linestyle='--', linewidth=1)
        plt.ylabel('CAR (%)')
        plt.xlabel('Year')
        plt.tight_layout()
        plt.savefig('car_boxplot.png', dpi=300)
        print("Saved car_boxplot.png")
        
    # 2. Plot Risk Changes
    if os.path.exists('risk_results_raw.csv'):
        risk_df = pd.read_csv('risk_results_raw.csv')
        
        # Melt the dataframe for easier plotting of multiple metrics
        risk_melt = pd.melt(risk_df, id_vars=['Event_Year', 'Bank'], 
                            value_vars=['Beta_Change', 'Corr_Change'],
                            var_name='Metric', value_name='Change')
                            
        plt.figure(figsize=(10, 6))
        sns.barplot(data=risk_melt, x='Event_Year', y='Change', hue='Metric', palette='Set2')
        plt.title('Change in Systematic Risk (Beta) and Systemic Risk (Correlation)', fontsize=14)
        plt.axhline(0, color='black', linestyle='--', linewidth=1)
        plt.ylabel('Change (Post-Event minus Pre-Event)')
        plt.xlabel('Year')
        plt.tight_layout()
        plt.savefig('risk_change_barplot.png', dpi=300)
        print("Saved risk_change_barplot.png")

if __name__ == "__main__":
    main()
