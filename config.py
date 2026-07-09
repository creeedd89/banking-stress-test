# Global Market Configuration

REGIONS = {
    "1": {
        "name": "United States",
        "index": "^GSPC", # S&P 500
        "banks": ["JPM", "BAC", "C", "WFC", "GS", "MS"]
    },
    "2": {
        "name": "United Kingdom",
        "index": "^FTSE", # FTSE 100
        "banks": ["HSBA.L", "BARC.L", "LLOY.L", "NWG.L"]
    },
    "3": {
        "name": "Europe (Eurozone)",
        "index": "^STOXX50E", # Euro Stoxx 50
        "banks": ["BNP.PA", "SAN.MC", "DBK.DE", "INGA.AS"]
    },
    "4": {
        "name": "Canada",
        "index": "^GSPTSE", # S&P/TSX Composite
        "banks": ["RY.TO", "TD.TO", "BNS.TO"]
    },
    "5": {
        "name": "Japan",
        "index": "^N225", # Nikkei 225
        "banks": ["8306.T", "8316.T", "8411.T"]
    },
    "6": {
        "name": "Custom Input",
        "index": None,
        "banks": []
    }
}

HISTORICAL_EVENTS = {
    "1": {"name": "Dot-Com Bubble Crash", "date": "2000-03-10"},
    "2": {"name": "September 11 Attacks", "date": "2001-09-17"}, # First trading day after
    "3": {"name": "Global Financial Crisis (Lehman)", "date": "2008-09-15"},
    "4": {"name": "US Credit Rating Downgrade", "date": "2011-08-05"},
    "5": {"name": "Brexit Vote", "date": "2016-06-24"}, # Day results were announced
    "6": {"name": "COVID-19 Market Crash", "date": "2020-02-20"},
    "7": {"name": "Silicon Valley Bank Collapse", "date": "2023-03-10"},
    "8": {"name": "Custom Date", "date": None}
}
