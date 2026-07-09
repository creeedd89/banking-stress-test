# 🌍 Global Market Event & Stress Test Analyzer (Streamlit App)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)
![Finance](https://img.shields.io/badge/Finance-Quantitative_Research-yellow.svg)

## 📌 Project Overview
How do global financial markets react to major historical events and stress tests? 

This project explores the **market impact of historical crashes, terrorist attacks, and financial frauds** across the globe. By utilizing quantitative finance techniques, it provides a highly informative, interactive **Streamlit Web Application** to fetch historical market data, perform event studies, and analyze changes in both systematic and systemic risks. 

You can now analyze major banks across dozens of countries, evaluating their reactions to specific national and global events like the **Enron Scandal, 2008 Financial Crisis, COVID-19, 2008 Mumbai Attacks, and the Fukushima Earthquake**!

## 🚀 Key Features

* **Modern Streamlit Dashboard (`app.py`)**: A stunning, dark-mode ready web interface built with Streamlit.
* **Massive Historical Database**: Features hundreds of curated events across categories like *Economic Crises, Natural Disasters, Terrorism & Wars, Political Shocks, and Frauds/Scams*.
* **Global Data Aggregation (`fetch_data.py`)**: Automatically retrieves historical banking data and market indices dating back to 1980.
* **Event Study Methodology (`event_study.py`)**: Calculates Cumulative Abnormal Returns (CAR) using customizable estimation and event windows.
* **Automated Rendering (`generate_report.py`)**: Generates high-quality visualizations of the selected event directly inside the web browser!

## 🛠️ Setup & Execution

### Prerequisites
Make sure you have Python installed, then set up your environment:
```bash
git clone https://github.com/creeedd89/banking-stress-test.git
cd banking-stress-test
pip install -r requirements.txt
```

### Running the Web App
Start the Streamlit server by running:
```bash
streamlit run app.py
```
This will automatically open the dashboard in your default web browser!

## 🤝 Let's Connect!
I completely overhauled this project into a fully-fledged global quantitative dashboard to deepen my understanding of quantitative finance, global history, and software engineering. If you found this interesting, feel free to connect with me!
