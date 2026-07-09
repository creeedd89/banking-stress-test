# Global Market Configuration by Continent

CONTINENTS = {
    "North America": {
        "United States": {
            "index": "^GSPC",
            "banks": ["JPM", "BAC", "C", "WFC", "GS", "MS"],
            "events": [
                {"name": "Dot-Com Bubble Crash", "date": "2000-03-10"},
                {"name": "September 11 Attacks", "date": "2001-09-17"},
                {"name": "Global Financial Crisis (Lehman)", "date": "2008-09-15"},
                {"name": "Silicon Valley Bank Collapse", "date": "2023-03-10"}
            ]
        },
        "Canada": {
            "index": "^GSPTSE",
            "banks": ["RY.TO", "TD.TO", "BNS.TO", "BMO.TO"],
            "events": [
                {"name": "2014 Oil Price Crash", "date": "2014-11-27"},
                {"name": "COVID-19 Market Crash", "date": "2020-02-20"}
            ]
        }
    },
    "Europe": {
        "United Kingdom": {
            "index": "^FTSE",
            "banks": ["HSBA.L", "BARC.L", "LLOY.L", "NWG.L"],
            "events": [
                {"name": "Black Wednesday", "date": "1992-09-16"},
                {"name": "Brexit Vote", "date": "2016-06-24"}
            ]
        },
        "Germany": {
            "index": "^GDAXI",
            "banks": ["DBK.DE", "CBK.DE"],
            "events": [
                {"name": "European Debt Crisis", "date": "2011-08-05"},
                {"name": "Wirecard Scandal", "date": "2020-06-18"}
            ]
        },
        "France": {
            "index": "^FCHI",
            "banks": ["BNP.PA", "GLE.PA", "ACA.PA"],
            "events": [
                {"name": "European Debt Crisis", "date": "2011-08-05"},
                {"name": "COVID-19 Market Crash", "date": "2020-02-20"}
            ]
        }
    },
    "Asia": {
        "Japan": {
            "index": "^N225",
            "banks": ["8306.T", "8316.T", "8411.T"],
            "events": [
                {"name": "Asset Price Bubble Collapse", "date": "1990-01-04"},
                {"name": "Fukushima Earthquake", "date": "2011-03-11"}
            ]
        },
        "China (Hong Kong)": {
            "index": "^HSI",
            "banks": ["0939.HK", "1398.HK", "3988.HK", "0005.HK"],
            "events": [
                {"name": "Chinese Stock Market Crash", "date": "2015-06-12"},
                {"name": "Evergrande Crisis", "date": "2021-09-20"}
            ]
        },
        "India": {
            "index": "^BSESN",
            "banks": ["HDFCBANK.BO", "SBIN.BO", "ICICIBANK.BO", "AXISBANK.BO"],
            "events": [
                {"name": "2008 Financial Crisis", "date": "2008-01-21"}, # Major drop in Indian markets
                {"name": "COVID-19 Market Crash", "date": "2020-03-23"}
            ]
        }
    },
    "South America": {
        "Brazil": {
            "index": "^BVSP",
            "banks": ["ITUB4.SA", "BBDC4.SA", "BBAS3.SA"],
            "events": [
                {"name": "2014-2016 Economic Crisis", "date": "2014-09-02"},
                {"name": "Joesley Day (Political Crisis)", "date": "2017-05-18"}
            ]
        },
        "Argentina": {
            "index": "MERV.BA",
            "banks": ["GGAL.BA", "BMA.BA", "BPAT.BA"],
            "events": [
                {"name": "2001 Debt Default", "date": "2001-12-01"},
                {"name": "2019 Primary Election Crash", "date": "2019-08-12"}
            ]
        }
    },
    "Africa": {
        "South Africa": {
            "index": "^J203.JO",
            "banks": ["SBK.JO", "FSR.JO", "ABG.JO"],
            "events": [
                {"name": "Nenegate (Finance Minister Fired)", "date": "2015-12-09"},
                {"name": "COVID-19 Market Crash", "date": "2020-03-15"}
            ]
        }
    },
    "Oceania": {
        "Australia": {
            "index": "^AXJO",
            "banks": ["CBA.AX", "WBC.AX", "NAB.AX", "ANZ.AX"],
            "events": [
                {"name": "1987 Black Monday", "date": "1987-10-20"},
                {"name": "COVID-19 Market Crash", "date": "2020-02-24"}
            ]
        }
    },
    "Antarctica": {
        "Penguin Exchange": {
            "index": "ICE",
            "banks": ["PENGUIN_BANK", "WALRUS_CREDIT"],
            "events": [
                {"name": "Great Ice Melt", "date": "2026-01-01"}
            ]
        }
    }
}
