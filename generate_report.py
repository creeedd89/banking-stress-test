import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_reports(event_name="Selected Event"):
    sns.set_theme(style="whitegrid")
    
    fig_car = None
    fig_risk = None
    
    # 1. Plot CARs
    if os.path.exists('car_results_raw.csv'):
        car_df = pd.read_csv('car_results_raw.csv')
        
        if not car_df.empty:
            car_df['CAR (%)'] = car_df['CAR'] * 100
            
            fig_car, ax_car = plt.subplots(figsize=(10, 6))
            sns.barplot(data=car_df, x='Bank', y='CAR (%)', hue='Bank', palette="vlag", legend=False, ax=ax_car)
            ax_car.set_title(f'Cumulative Abnormal Returns (CAR)\nEvent: {event_name}', fontsize=14)
            ax_car.axhline(0, color='black', linestyle='--', linewidth=1)
            ax_car.set_ylabel('CAR (%)')
            ax_car.set_xlabel('Bank')
            ax_car.tick_params(axis='x', rotation=45)
            fig_car.tight_layout()
            fig_car.savefig('car_boxplot.png', dpi=300)
        else:
            print("No CAR data to plot.")
        
    # 2. Plot Risk Changes
    if os.path.exists('risk_results_raw.csv'):
        risk_df = pd.read_csv('risk_results_raw.csv')
        
        if not risk_df.empty:
            risk_melt = pd.melt(risk_df, id_vars=['Bank'], 
                                value_vars=['Beta_Change', 'Corr_Change'],
                                var_name='Metric', value_name='Change')
                                
            fig_risk, ax_risk = plt.subplots(figsize=(12, 6))
            sns.barplot(data=risk_melt, x='Bank', y='Change', hue='Metric', palette='Set2', ax=ax_risk)
            ax_risk.set_title(f'Change in Systematic (Beta) vs Systemic (Correlation) Risk\nEvent: {event_name}', fontsize=14)
            ax_risk.axhline(0, color='black', linestyle='--', linewidth=1)
            ax_risk.set_ylabel('Change (Post-Event minus Pre-Event)')
            ax_risk.set_xlabel('Bank')
            ax_risk.tick_params(axis='x', rotation=45)
            fig_risk.tight_layout()
            fig_risk.savefig('risk_change_barplot.png', dpi=300)
        else:
            print("No Risk data to plot.")

    return fig_car, fig_risk

if __name__ == "__main__":
    generate_reports()
