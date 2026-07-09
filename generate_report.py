import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_reports(event_name="Selected Event"):
    sns.set_theme(style="whitegrid")
    
    # 1. Plot CARs
    if os.path.exists('car_results_raw.csv'):
        car_df = pd.read_csv('car_results_raw.csv')
        
        if not car_df.empty:
            # Convert CAR to percentage
            car_df['CAR (%)'] = car_df['CAR'] * 100
            
            plt.figure(figsize=(10, 6))
            sns.barplot(data=car_df, x='Bank', y='CAR (%)', palette="vlag")
            plt.title(f'Cumulative Abnormal Returns (CAR)\nEvent: {event_name}', fontsize=14)
            plt.axhline(0, color='black', linestyle='--', linewidth=1)
            plt.ylabel('CAR (%)')
            plt.xlabel('Bank')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('car_boxplot.png', dpi=300)
            print("Saved car_boxplot.png")
        else:
            print("No CAR data to plot.")
        
    # 2. Plot Risk Changes
    if os.path.exists('risk_results_raw.csv'):
        risk_df = pd.read_csv('risk_results_raw.csv')
        
        if not risk_df.empty:
            # Melt the dataframe for easier plotting of multiple metrics
            risk_melt = pd.melt(risk_df, id_vars=['Bank'], 
                                value_vars=['Beta_Change', 'Corr_Change'],
                                var_name='Metric', value_name='Change')
                                
            plt.figure(figsize=(12, 6))
            sns.barplot(data=risk_melt, x='Bank', y='Change', hue='Metric', palette='Set2')
            plt.title(f'Change in Systematic (Beta) vs Systemic (Correlation) Risk\nEvent: {event_name}', fontsize=14)
            plt.axhline(0, color='black', linestyle='--', linewidth=1)
            plt.ylabel('Change (Post-Event minus Pre-Event)')
            plt.xlabel('Bank')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('risk_change_barplot.png', dpi=300)
            print("Saved risk_change_barplot.png")
        else:
            print("No Risk data to plot.")

if __name__ == "__main__":
    generate_reports()
