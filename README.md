# 🌍 Global Market Event & Stress Test Analyzer (Desktop App)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blueviolet.svg)
![Finance](https://img.shields.io/badge/Finance-Quantitative_Research-yellow.svg)

## 📌 Project Overview
How do global financial markets react to major historical events and stress tests? 

This project explores the **market impact of historical crashes and regulatory stress tests** across the globe. By utilizing quantitative finance techniques, it provides a complete, interactive **Desktop Application** to fetch historical market data, perform event studies, and analyze changes in both systematic and systemic risks. 

You can now analyze major banks across all **7 Continents**, evaluating their reactions to specific national and global events like the **Dot-Com Bubble, 2008 Financial Crisis, COVID-19, Brexit, and the Fukushima Earthquake**!

## 🚀 Key Features

* **Desktop GUI App (`app.py`)**: A native Windows application built with `Tkinter`. No more terminal commands! Select your Continent, Country, and Event from easy-to-use dropdown menus.
* **Global Data Aggregation (`fetch_data.py`)**: Automatically retrieves historical banking data and market indices (S&P 500, FTSE 100, Euro Stoxx 50, Nikkei 225, etc.) dating back to 1980.
* **Event Study Methodology (`event_study.py`)**: Calculates Cumulative Abnormal Returns (CAR) using customizable estimation and event windows.
* **Risk Analytics (`risk_analysis.py`)**: Computes pre- and post-event changes in Systematic Risk (Beta) and Systemic Risk (Correlation).
* **Automated Reporting (`generate_report.py`)**: Generates high-quality visualizations of the selected event using `Seaborn`, and automatically pops them open for you to view.

## 🌐 Supported Continents & Countries
- **North America**: USA (S&P 500), Canada (TSX)
- **Europe**: UK (FTSE 100), Germany (DAX), France (CAC 40)
- **Asia**: Japan (Nikkei 225), China/HK (Hang Seng), India (BSE SENSEX)
- **South America**: Brazil (Bovespa), Argentina (Merval)
- **Africa**: South Africa (JSE)
- **Oceania**: Australia (ASX 200)
- **Antarctica**: (Included for fun—waiting for the Penguin Exchange to list!)

## 🛠️ Setup & Execution

### Prerequisites
Make sure you have Python installed, then set up your environment:
```bash
git clone https://github.com/creeedd89/banking-stress-test.git
cd banking-stress-test
pip install -r requirements.txt
```

### Running the Desktop App
Start the analyzer by running:
```bash
python app.py
```
A desktop window will open. Follow the dropdowns to select your region and event, hit "Run Analysis", and the application will automatically pop open `.png` charts of the results once complete!

## 🤝 Let's Connect!
I completely overhauled this project from a static terminal script into a fully-fledged global desktop application to deepen my understanding of quantitative finance and software engineering. If you found this interesting, feel free to connect with me!
