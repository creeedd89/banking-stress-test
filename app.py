import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from config import CONTINENTS
from fetch_data import fetch_data_for_region
from event_study import run_event_study
from risk_analysis import run_risk_analysis
from generate_report import generate_reports

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Event Study Analyzer")
        self.root.geometry("600x500")
        
        # UI Setup
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Continent
        ttk.Label(main_frame, text="Select Continent:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.continent_var = tk.StringVar()
        self.continent_cb = ttk.Combobox(main_frame, textvariable=self.continent_var, state="readonly", width=30)
        self.continent_cb['values'] = list(CONTINENTS.keys())
        self.continent_cb.grid(row=0, column=1, sticky=tk.EW, pady=5)
        self.continent_cb.bind('<<ComboboxSelected>>', self.on_continent_select)
        
        # Country
        ttk.Label(main_frame, text="Select Country:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.country_var = tk.StringVar()
        self.country_cb = ttk.Combobox(main_frame, textvariable=self.country_var, state="readonly", width=30)
        self.country_cb.grid(row=1, column=1, sticky=tk.EW, pady=5)
        self.country_cb.bind('<<ComboboxSelected>>', self.on_country_select)
        
        # Event
        ttk.Label(main_frame, text="Select Historical Event:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.event_var = tk.StringVar()
        self.event_cb = ttk.Combobox(main_frame, textvariable=self.event_var, state="readonly", width=30)
        self.event_cb.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # Estimation Window
        ttk.Label(main_frame, text="Estimation Window (days):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.window_var = tk.StringVar(value="255")
        ttk.Entry(main_frame, textvariable=self.window_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Gap
        ttk.Label(main_frame, text="Gap (days):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.gap_var = tk.StringVar(value="10")
        ttk.Entry(main_frame, textvariable=self.gap_var, width=10).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('Helvetica', 10, 'italic'))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Run Button
        self.run_btn = ttk.Button(main_frame, text="Run Analysis", command=self.run_analysis)
        self.run_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
    def on_continent_select(self, event):
        continent = self.continent_var.get()
        if continent:
            countries = list(CONTINENTS[continent].keys())
            self.country_cb['values'] = countries
            self.country_cb.set('')
            self.event_cb['values'] = []
            self.event_cb.set('')
            
    def on_country_select(self, event):
        continent = self.continent_var.get()
        country = self.country_var.get()
        if continent and country:
            events = CONTINENTS[continent][country]["events"]
            event_names = [e["name"] for e in events]
            self.event_cb['values'] = event_names
            if event_names:
                self.event_cb.current(0)
                
    def get_event_date(self, continent, country, event_name):
        events = CONTINENTS[continent][country]["events"]
        for e in events:
            if e["name"] == event_name:
                return e["date"]
        return None

    def run_analysis(self):
        continent = self.continent_var.get()
        country = self.country_var.get()
        event_name = self.event_var.get()
        
        if not continent or not country or not event_name:
            messagebox.showwarning("Input Error", "Please select a Continent, Country, and Event.")
            return
            
        if continent == "Antarctica":
            messagebox.showinfo("Antarctica", "Penguins do not have a functional stock market... yet! Try another continent.")
            return
            
        try:
            window = int(self.window_var.get())
            gap = int(self.gap_var.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Window and Gap must be integers.")
            return
            
        self.run_btn.config(state=tk.DISABLED)
        self.status_var.set("Running pipeline... Please wait.")
        
        # Run in thread so GUI doesn't freeze
        thread = threading.Thread(target=self.pipeline_thread, args=(continent, country, event_name, window, gap))
        thread.start()
        
    def pipeline_thread(self, continent, country, event_name, window, gap):
        try:
            country_data = CONTINENTS[continent][country]
            market_index = country_data["index"]
            bank_tickers = country_data["banks"]
            event_date = self.get_event_date(continent, country, event_name)
            
            self.status_var.set(f"[1/4] Fetching data for {country} ({market_index})...")
            success = fetch_data_for_region(market_index, bank_tickers, start_date="1980-01-01")
            
            if not success:
                self.root.after(0, self.update_status, "Failed to fetch data.")
                return
                
            self.status_var.set("[2/4] Running Event Study (CAR)...")
            run_event_study(event_date, event_name, market_col=market_index, est_window=window, gap=gap)
            
            self.status_var.set("[3/4] Running Risk Analysis (Beta & Correlation)...")
            run_risk_analysis(event_date, event_name, market_col=market_index, window=window, gap=gap)
            
            self.status_var.set("[4/4] Generating Reports...")
            generate_reports(event_name)
            
            self.root.after(0, self.update_status, f"Success! Generated reports for {event_name}.")
            
            # Open images
            if os.name == 'nt':
                os.startfile('car_boxplot.png')
                os.startfile('risk_change_barplot.png')
                
        except Exception as e:
            self.root.after(0, self.update_status, f"Error: {e}")
            
    def update_status(self, message):
        self.status_var.set(message)
        self.run_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
