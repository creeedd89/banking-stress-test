import os

NEW_CONFIG = """# Global Market Configuration by Continent (Massive Exhaustive Database)

CONTINENTS = {
    "North America": {
        "United States": {
            "index": "^GSPC",
            "banks": ["JPM", "BAC", "C", "WFC", "GS", "MS", "USB", "PNC"],
            "events": [
                {"name": "Black Monday", "date": "1987-10-19", "category": "Economic Crisis"},
                {"name": "Dot-Com Bubble Crash", "date": "2000-03-10", "category": "Economic Crisis"},
                {"name": "September 11 Attacks", "date": "2001-09-17", "category": "Terrorism/War"},
                {"name": "Enron Scandal Bankruptcy", "date": "2001-12-02", "category": "Fraud/Scam"},
                {"name": "Global Financial Crisis (Lehman)", "date": "2008-09-15", "category": "Economic Crisis"},
                {"name": "Flash Crash of 2010", "date": "2010-05-06", "category": "Economic Crisis"},
                {"name": "US Credit Rating Downgrade", "date": "2011-08-05", "category": "Economic Crisis"},
                {"name": "Trump Election Victory", "date": "2016-11-09", "category": "Political Shock"},
                {"name": "US-China Tariff Enactment", "date": "2018-07-06", "category": "Political Shock"},
                {"name": "COVID-19 Market Crash", "date": "2020-03-09", "category": "Economic Crisis"},
                {"name": "Silicon Valley Bank Collapse", "date": "2023-03-10", "category": "Fraud/Scam"},
                {"name": "2024 US Presidential Election Shock", "date": "2024-11-06", "category": "Political Shock"},
                {"name": "Commercial Real Estate Crash", "date": "2025-05-15", "category": "Economic Crisis"},
                {"name": "AI Tech Bubble Correction", "date": "2026-03-12", "category": "Economic Crisis"}
            ]
        },
        "Canada": {
            "index": "^GSPTSE",
            "banks": ["RY.TO", "TD.TO", "BNS.TO", "BMO.TO", "CM.TO"],
            "events": [
                {"name": "2014 Oil Price Crash", "date": "2014-11-27", "category": "Economic Crisis"},
                {"name": "COVID-19 Market Crash", "date": "2020-02-20", "category": "Economic Crisis"},
                {"name": "Sino-Forest Fraud Collapse", "date": "2011-06-02", "category": "Fraud/Scam"},
                {"name": "Parliament Hill Attack", "date": "2014-10-22", "category": "Terrorism/War"}
            ]
        },
        "Mexico": {
            "index": "^MXX",
            "banks": ["GFNORTEO.MX", "BBAJIOO.MX", "BSMXB.MX"],
            "events": [
                {"name": "Tequila Crisis (Peso Devaluation)", "date": "1994-12-20", "category": "Economic Crisis"},
                {"name": "COVID-19 Crash", "date": "2020-02-20", "category": "Economic Crisis"},
                {"name": "NAFTA Renegotiation Fears", "date": "2016-11-09", "category": "Political Shock"}
            ]
        }
    },
    "Europe": {
        "United Kingdom": {
            "index": "^FTSE",
            "banks": ["HSBA.L", "BARC.L", "LLOY.L", "NWG.L", "STAN.L"],
            "events": [
                {"name": "Black Wednesday", "date": "1992-09-16", "category": "Economic Crisis"},
                {"name": "Northern Rock Bank Run", "date": "2007-09-14", "category": "Economic Crisis"},
                {"name": "7/7 London Bombings", "date": "2005-07-07", "category": "Terrorism/War"},
                {"name": "Brexit Vote Shock", "date": "2016-06-24", "category": "Political Shock"},
                {"name": "Truss Mini-Budget Crash", "date": "2022-09-23", "category": "Political Shock"},
                {"name": "UK Gilt Yield Spike", "date": "2025-10-31", "category": "Economic Crisis"}
            ]
        },
        "Germany": {
            "index": "^GDAXI",
            "banks": ["DBK.DE", "CBK.DE"],
            "events": [
                {"name": "European Debt Crisis", "date": "2011-08-05", "category": "Economic Crisis"},
                {"name": "Wirecard Fraud Collapse", "date": "2020-06-18", "category": "Fraud/Scam"},
                {"name": "Volkswagen Emissions Scandal", "date": "2015-09-18", "category": "Fraud/Scam"},
                {"name": "German Auto Industry Bailout", "date": "2025-09-18", "category": "Economic Crisis"}
            ]
        },
        "France": {
            "index": "^FCHI",
            "banks": ["BNP.PA", "GLE.PA", "ACA.PA"],
            "events": [
                {"name": "European Debt Crisis", "date": "2011-08-05", "category": "Economic Crisis"},
                {"name": "Société Générale Trading Scandal (Kerviel)", "date": "2008-01-24", "category": "Fraud/Scam"},
                {"name": "November 2015 Paris Attacks", "date": "2015-11-16", "category": "Terrorism/War"}
            ]
        },
        "Italy": {
            "index": "FTSEMIB.MI",
            "banks": ["ISP.MI", "UCG.MI", "MB.MI"],
            "events": [
                {"name": "Eurozone Debt Crisis Peak", "date": "2011-11-09", "category": "Economic Crisis"},
                {"name": "Parmalat Bankruptcy Fraud", "date": "2003-12-19", "category": "Fraud/Scam"}
            ]
        },
        "Switzerland": {
            "index": "^SSMI",
            "banks": ["UBSG.SW", "CSGN.SW"],
            "events": [
                {"name": "Swiss Franc Peg Removal Shock", "date": "2015-01-15", "category": "Economic Crisis"},
                {"name": "Credit Suisse Collapse", "date": "2023-03-15", "category": "Economic Crisis"}
            ]
        }
    },
    "Middle East": {
        "Israel": {
            "index": "TA35.TA",
            "banks": ["LUMI.TA", "POLI.TA", "DSCT.TA", "FIBI.TA"],
            "events": [
                {"name": "Oslo Accords Announcement", "date": "1993-09-13", "category": "Political Shock"},
                {"name": "Second Lebanon War Starts", "date": "2006-07-12", "category": "Terrorism/War"},
                {"name": "October 7 Attacks", "date": "2023-10-08", "category": "Terrorism/War"},
                {"name": "Operation Sindoor", "date": "2024-02-15", "category": "Terrorism/War"}
            ]
        },
        "Saudi Arabia": {
            "index": "^TASI.SR",
            "banks": ["1120.SR", "1180.SR", "1010.SR"],
            "events": [
                {"name": "Abqaiq-Khurais Drone Attack", "date": "2019-09-15", "category": "Terrorism/War"},
                {"name": "OPEC+ Oil Price War", "date": "2020-03-09", "category": "Economic Crisis"},
                {"name": "Saudi Aramco Historic IPO", "date": "2019-12-11", "category": "Economic Crisis"}
            ]
        },
        "Lebanon": {
            "index": "BLOM.BY", 
            "banks": ["AUDI.BY", "BLOM.BY"],
            "events": [
                {"name": "2006 Lebanon War", "date": "2006-07-12", "category": "Terrorism/War"},
                {"name": "Port of Beirut Explosion", "date": "2020-08-04", "category": "Natural Disaster"},
                {"name": "Lebanese Liquidity Crisis Peak", "date": "2019-10-17", "category": "Economic Crisis"}
            ]
        },
        "United Arab Emirates": {
            "index": "^DFMGI",
            "banks": ["EMIRATESNBD.AE", "FAB.AD"],
            "events": [
                {"name": "Dubai Debt Standstill Crisis", "date": "2009-11-25", "category": "Economic Crisis"}
            ]
        }
    },
    "Asia": {
        "Japan": {
            "index": "^N225",
            "banks": ["8306.T", "8316.T", "8411.T"],
            "events": [
                {"name": "Asset Price Bubble Collapse", "date": "1990-01-04", "category": "Economic Crisis"},
                {"name": "Asian Financial Crisis", "date": "1997-11-24", "category": "Economic Crisis"},
                {"name": "BOJ Introduces Quantitative Easing", "date": "2001-03-19", "category": "Economic Crisis"},
                {"name": "Fukushima Earthquake & Tsunami", "date": "2011-03-11", "category": "Natural Disaster"},
                {"name": "Shinzo Abe Assassination", "date": "2022-07-08", "category": "Political Shock"},
                {"name": "Historic BOJ Rate Hike", "date": "2025-04-01", "category": "Economic Crisis"}
            ]
        },
        "China (Hong Kong)": {
            "index": "^HSI",
            "banks": ["0939.HK", "1398.HK", "3988.HK", "0005.HK"],
            "events": [
                {"name": "Asian Financial Crisis", "date": "1997-10-23", "category": "Economic Crisis"},
                {"name": "Chinese Stock Market Crash", "date": "2015-06-12", "category": "Economic Crisis"},
                {"name": "PBOC Yuan Devaluation", "date": "2015-08-11", "category": "Economic Crisis"},
                {"name": "Evergrande Liquidity Crisis", "date": "2021-09-20", "category": "Economic Crisis"},
                {"name": "Taiwan Blockade Military Drills", "date": "2025-08-08", "category": "Political Shock"}
            ]
        },
        "India": {
            "index": "^BSESN",
            "banks": ["HDFCBANK.BO", "SBIN.BO", "ICICIBANK.BO", "AXISBANK.BO", "KOTAKBANK.BO"],
            "events": [
                {"name": "1991 Economic Reforms Budget", "date": "1991-07-24", "category": "Political Shock"},
                {"name": "2008 Financial Crisis", "date": "2008-01-21", "category": "Economic Crisis"},
                {"name": "2008 Mumbai Attacks", "date": "2008-11-28", "category": "Terrorism/War"},
                {"name": "Satyam Computer Scam", "date": "2009-01-07", "category": "Fraud/Scam"},
                {"name": "Demonetization Announcement", "date": "2016-11-09", "category": "Economic Crisis"},
                {"name": "Punjab National Bank Scam", "date": "2018-02-14", "category": "Fraud/Scam"},
                {"name": "Adani Group Hindenburg Report", "date": "2023-01-25", "category": "Fraud/Scam"},
                {"name": "2024 Election Results Shock", "date": "2024-06-04", "category": "Political Shock"},
                {"name": "Historic RBI Rate Cut Cycle", "date": "2025-02-01", "category": "Economic Crisis"}
            ]
        },
        "South Korea": {
            "index": "^KS11",
            "banks": ["105560.KS", "055550.KS", "316140.KS"],
            "events": [
                {"name": "IMF Bailout (Asian Crisis)", "date": "1997-11-21", "category": "Economic Crisis"},
                {"name": "North Korea Nuclear Test", "date": "2017-09-04", "category": "Terrorism/War"}
            ]
        }
    },
    "South America": {
        "Brazil": {
            "index": "^BVSP",
            "banks": ["ITUB4.SA", "BBDC4.SA", "BBAS3.SA"],
            "events": [
                {"name": "2014-2016 Economic Crisis", "date": "2014-09-02", "category": "Economic Crisis"},
                {"name": "Petrobras Operation Car Wash", "date": "2014-03-17", "category": "Fraud/Scam"},
                {"name": "Joesley Day", "date": "2017-05-18", "category": "Political Shock"},
                {"name": "Brumadinho Dam Disaster", "date": "2019-01-28", "category": "Natural Disaster"}
            ]
        },
        "Argentina": {
            "index": "MERV.BA",
            "banks": ["GGAL.BA", "BMA.BA", "BPAT.BA"],
            "events": [
                {"name": "2001 Debt Default", "date": "2001-12-03", "category": "Economic Crisis"},
                {"name": "2019 Primary Election Crash", "date": "2019-08-12", "category": "Political Shock"}
            ]
        }
    },
    "Africa": {
        "South Africa": {
            "index": "^J203.JO",
            "banks": ["SBK.JO", "FSR.JO", "ABG.JO", "NED.JO"],
            "events": [
                {"name": "Nenegate (Finance Minister Fired)", "date": "2015-12-09", "category": "Political Shock"},
                {"name": "Steinhoff Accounting Fraud", "date": "2017-12-06", "category": "Fraud/Scam"},
                {"name": "2021 July Unrest / Riots", "date": "2021-07-12", "category": "Terrorism/War"}
            ]
        },
        "Egypt": {
            "index": "^CASE30",
            "banks": ["COMI.CA", "QNBA.CA"],
            "events": [
                {"name": "2011 Egyptian Revolution (Market Reopen)", "date": "2011-03-23", "category": "Political Shock"},
                {"name": "2016 Currency Devaluation", "date": "2016-11-03", "category": "Economic Crisis"}
            ]
        },
        "Tunisia": {
            "index": "^TUNINDEX",
            "banks": ["BIAT.TN", "AMEN.TN", "AB.TN"],
            "events": [
                {"name": "Jasmine Revolution (Arab Spring begins)", "date": "2010-12-17", "category": "Political Shock"},
                {"name": "Presidential Power Seizure", "date": "2021-07-25", "category": "Political Shock"}
            ]
        },
        "Senegal": {
            "index": "^BRVM",
            "banks": ["ETI.CI", "BOAS.SN", "SGBC.CI"],
            "events": [
                {"name": "CFA Franc Devaluation", "date": "1994-01-12", "category": "Economic Crisis"},
                {"name": "2021 Senegalese Protests", "date": "2021-03-03", "category": "Political Shock"},
                {"name": "Presidential Election Delay Turmoil", "date": "2024-02-03", "category": "Political Shock"}
            ]
        }
    },
    "Oceania": {
        "Australia": {
            "index": "^AXJO",
            "banks": ["CBA.AX", "WBC.AX", "NAB.AX", "ANZ.AX"],
            "events": [
                {"name": "1987 Black Monday", "date": "1987-10-20", "category": "Economic Crisis"},
                {"name": "AMP Royal Commission Scandal", "date": "2018-04-17", "category": "Fraud/Scam"},
                {"name": "2014 Sydney Hostage Crisis", "date": "2014-12-15", "category": "Terrorism/War"}
            ]
        }
    }
}
"""

with open("d:\\banking stress test\\config.py", "w", encoding='utf-8') as f:
    f.write(NEW_CONFIG)

print("SUCCESS")
