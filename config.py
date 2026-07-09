# Global Market Configuration by Continent (Massive Database Expansion)

CONTINENTS = {
    "North America": {
        "United States": {
            "index": "^GSPC",
            "banks": ["JPM", "BAC", "C", "WFC", "GS", "MS", "USB", "PNC"],
            "events": [
                # Economic/Financial Crises
                {"name": "Dot-Com Bubble Crash", "date": "2000-03-10", "category": "Economic Crisis"},
                {"name": "Global Financial Crisis (Lehman)", "date": "2008-09-15", "category": "Economic Crisis"},
                {"name": "Flash Crash of 2010", "date": "2010-05-06", "category": "Economic Crisis"},
                {"name": "US Credit Rating Downgrade", "date": "2011-08-05", "category": "Economic Crisis"},
                {"name": "COVID-19 Market Crash", "date": "2020-02-20", "category": "Economic Crisis"},
                # Frauds & Scams
                {"name": "Enron Scandal Bankruptcy", "date": "2001-12-02", "category": "Fraud/Scam"},
                {"name": "Bernie Madoff Arrest", "date": "2008-12-11", "category": "Fraud/Scam"},
                {"name": "FTX Collapse", "date": "2022-11-11", "category": "Fraud/Scam"},
                {"name": "Silicon Valley Bank Collapse", "date": "2023-03-10", "category": "Fraud/Scam"},
                # Terrorism & Wars
                {"name": "September 11 Attacks", "date": "2001-09-17", "category": "Terrorism/War"}, # First day market reopened
                {"name": "Boston Marathon Bombing", "date": "2013-04-15", "category": "Terrorism/War"},
                # Natural Disasters
                {"name": "Hurricane Katrina", "date": "2005-08-29", "category": "Natural Disaster"},
                # Political Shocks
                {"name": "Trump Election Victory", "date": "2016-11-09", "category": "Political Shock"}
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
                {"name": "Brexit Vote Shock", "date": "2016-06-24", "category": "Political Shock"},
                {"name": "Truss Mini-Budget Crash", "date": "2022-09-23", "category": "Political Shock"},
                {"name": "7/7 London Bombings", "date": "2005-07-07", "category": "Terrorism/War"},
                {"name": "Barclays LIBOR Scandal", "date": "2012-06-27", "category": "Fraud/Scam"}
            ]
        },
        "Germany": {
            "index": "^GDAXI",
            "banks": ["DBK.DE", "CBK.DE"],
            "events": [
                {"name": "European Debt Crisis", "date": "2011-08-05", "category": "Economic Crisis"},
                {"name": "Wirecard Fraud Collapse", "date": "2020-06-18", "category": "Fraud/Scam"},
                {"name": "Volkswagen Emissions Scandal", "date": "2015-09-18", "category": "Fraud/Scam"},
                {"name": "Berlin Christmas Market Attack", "date": "2016-12-19", "category": "Terrorism/War"}
            ]
        },
        "France": {
            "index": "^FCHI",
            "banks": ["BNP.PA", "GLE.PA", "ACA.PA"],
            "events": [
                {"name": "European Debt Crisis", "date": "2011-08-05", "category": "Economic Crisis"},
                {"name": "Société Générale Trading Scandal (Kerviel)", "date": "2008-01-24", "category": "Fraud/Scam"},
                {"name": "November 2015 Paris Attacks", "date": "2015-11-16", "category": "Terrorism/War"}, # First trading day after
                {"name": "Charlie Hebdo Attack", "date": "2015-01-07", "category": "Terrorism/War"}
            ]
        },
        "Italy": {
            "index": "FTSEMIB.MI",
            "banks": ["ISP.MI", "UCG.MI", "MB.MI"],
            "events": [
                {"name": "Eurozone Debt Crisis Peak", "date": "2011-11-09", "category": "Economic Crisis"},
                {"name": "Parmalat Bankruptcy Fraud", "date": "2003-12-19", "category": "Fraud/Scam"},
                {"name": "COVID-19 Initial Outbreak Lockdown", "date": "2020-02-24", "category": "Economic Crisis"}
            ]
        },
        "Switzerland": {
            "index": "^SSMI",
            "banks": ["UBSG.SW", "CSGN.SW"], # Note: CSGN delisted recently, but historical data exists
            "events": [
                {"name": "Swiss Franc Peg Removal Shock", "date": "2015-01-15", "category": "Economic Crisis"},
                {"name": "Credit Suisse Collapse", "date": "2023-03-15", "category": "Economic Crisis"}
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
                {"name": "Fukushima Earthquake & Tsunami", "date": "2011-03-11", "category": "Natural Disaster"},
                {"name": "Shinzo Abe Assassination", "date": "2022-07-08", "category": "Political Shock"},
                {"name": "Olympus Accounting Scandal", "date": "2011-11-08", "category": "Fraud/Scam"}
            ]
        },
        "China (Hong Kong)": {
            "index": "^HSI",
            "banks": ["0939.HK", "1398.HK", "3988.HK", "0005.HK"],
            "events": [
                {"name": "Asian Financial Crisis", "date": "1997-10-23", "category": "Economic Crisis"},
                {"name": "Chinese Stock Market Crash", "date": "2015-06-12", "category": "Economic Crisis"},
                {"name": "Evergrande Liquidity Crisis", "date": "2021-09-20", "category": "Economic Crisis"},
                {"name": "Hong Kong Protests Escalation", "date": "2019-08-05", "category": "Political Shock"}
            ]
        },
        "India": {
            "index": "^BSESN",
            "banks": ["HDFCBANK.BO", "SBIN.BO", "ICICIBANK.BO", "AXISBANK.BO", "KOTAKBANK.BO"],
            "events": [
                {"name": "2008 Financial Crisis", "date": "2008-01-21", "category": "Economic Crisis"},
                {"name": "Demonetization Announcement", "date": "2016-11-09", "category": "Economic Crisis"},
                {"name": "Satyam Computer Scam", "date": "2009-01-07", "category": "Fraud/Scam"},
                {"name": "Punjab National Bank (Nirav Modi) Scam", "date": "2018-02-14", "category": "Fraud/Scam"},
                {"name": "Adani Group Hindenburg Report", "date": "2023-01-25", "category": "Fraud/Scam"},
                {"name": "2008 Mumbai Attacks", "date": "2008-11-28", "category": "Terrorism/War"} # First trading day post-attack
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
                {"name": "Joesley Day (Presidential Corruption Shock)", "date": "2017-05-18", "category": "Political Shock"},
                {"name": "Petrobras Operation Car Wash Scandal", "date": "2014-03-17", "category": "Fraud/Scam"},
                {"name": "Brumadinho Dam Disaster", "date": "2019-01-28", "category": "Natural Disaster"}
            ]
        },
        "Argentina": {
            "index": "MERV.BA",
            "banks": ["GGAL.BA", "BMA.BA", "BPAT.BA"],
            "events": [
                {"name": "2001 Debt Default (Corralito)", "date": "2001-12-03", "category": "Economic Crisis"},
                {"name": "2019 Primary Election Crash", "date": "2019-08-12", "category": "Political Shock"}
            ]
        },
        "Chile": {
            "index": "^IPSA",
            "banks": ["BSANTANDER.SN", "CHILE.SN", "BCI.SN"],
            "events": [
                {"name": "2019 Chilean Social Protests", "date": "2019-10-18", "category": "Political Shock"},
                {"name": "2010 Chilean Earthquake", "date": "2010-03-01", "category": "Natural Disaster"}
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
        }
    },
    "Oceania": {
        "Australia": {
            "index": "^AXJO",
            "banks": ["CBA.AX", "WBC.AX", "NAB.AX", "ANZ.AX"],
            "events": [
                {"name": "1987 Black Monday", "date": "1987-10-20", "category": "Economic Crisis"},
                {"name": "COVID-19 Market Crash", "date": "2020-02-24", "category": "Economic Crisis"},
                {"name": "AMP Royal Commission Scandal", "date": "2018-04-17", "category": "Fraud/Scam"},
                {"name": "2014 Sydney Hostage Crisis", "date": "2014-12-15", "category": "Terrorism/War"}
            ]
        },
        "New Zealand": {
            "index": "^NZ50",
            "banks": ["ANZ.NZ", "WBC.NZ"],
            "events": [
                {"name": "Christchurch Earthquake", "date": "2011-02-22", "category": "Natural Disaster"},
                {"name": "Christchurch Mosque Shootings", "date": "2019-03-15", "category": "Terrorism/War"}
            ]
        }
    }
}
