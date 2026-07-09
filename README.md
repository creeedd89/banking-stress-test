# 🌍 Global Market Event & Stress Test Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-green.svg)
![Finance](https://img.shields.io/badge/Finance-Quantitative_Research-yellow.svg)

## 📌 Project Overview
How do global financial markets react to major historical events and stress tests? 

This project explores the **market impact of historical crashes and regulatory stress tests** across the globe. By utilizing quantitative finance techniques, it provides a complete, interactive pipeline to fetch historical market data, perform event studies, and analyze changes in both systematic and systemic risks. 

You can now analyze major banks across the **US, UK, Europe, Canada, and Japan**, and evaluate their reactions to events like the **Dot-Com Bubble, 2008 Financial Crisis, COVID-19, and the Silicon Valley Bank collapse**!

## 🚀 Key Features

* **Interactive CLI (`main.py`)**: A fully interactive terminal app that lets you choose the country, the market index, and the historical event to analyze.
* **Global Data Aggregation (`fetch_data.py`)**: Automatically retrieves historical banking data and market indices (S&P 500, FTSE 100, Euro Stoxx 50, etc.) dating back to 1999.
* **Event Study Methodology (`event_study.py`)**: Calculates Cumulative Abnormal Returns (CAR) using customizable estimation and event windows.
* **Risk Analytics (`risk_analysis.py`)**: Computes pre- and post-event changes in:
  * **Systematic Risk (Beta)**: The bank's volatility relative to its regional market index.
  * **Systemic Risk (Correlation)**: The interconnectedness of bank returns.
* **Automated Reporting (`generate_report.py`)**: Generates dynamic, high-quality visualizations of the selected event using `Seaborn`.

## 🌐 Supported Global Markets
- **United States** (S&P 500)
- **United Kingdom** (FTSE 100)
- **Europe (Eurozone)** (Euro Stoxx 50)
- **Canada** (S&P/TSX Composite)
- **Japan** (Nikkei 225)
- **Custom Input**: Manually enter any Yahoo Finance index and bank tickers!

## 🛠️ Setup & Execution

### Prerequisites
Make sure you have Python installed, then set up your environment:
```bash
git clone https://github.com/creeedd89/banking-stress-test.git
cd banking-stress-test
pip install -r requirements.txt
```

### Running the Interactive App
Start the analyzer by simply running:
```bash
python main.py
```
Follow the on-screen prompts to select your region, event, and analysis windows. The script will automatically fetch data, run the quantitative models, and output `.png` charts of the results.

## 🤝 Let's Connect!
I expanded this project globally to deepen my understanding of quantitative finance, global markets, and interactive data science. If you found this interesting or want to discuss financial modeling, feel free to connect with me!
