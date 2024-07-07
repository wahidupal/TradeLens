import yfinance as yf
import streamlit as st
import time
import pandas as pd
from streamlit_option_menu import option_menu
import numpy as np
from datetime import date,datetime,timedelta
from plotly import graph_objs as go
from prophet import Prophet


st.set_page_config(page_title="Stock Analysis", page_icon=":chart_with_upwards_trend:")

st.title("Stocks Analysis")
st.caption("Stock Price Analysis and Price forecasting of National Stock Exchange (NSE) and Bombay Stock Exchange (BSE) listed Companies.")
st.write("---")

with st.sidebar:
    selected=option_menu(
    menu_title="Menu",
    options=["HOME","LIVE PRICES","GRAPHS","DATA","INFORMATION","TECHNICAL INDICATORS","FORECAST","HELP"],
    icons=["house","activity","graph-up","clipboard-data","info-circle","clipboard-pulse","bar-chart-line","question-circle"],menu_icon="shop-window")
    st.write("---")
    

company = ("", "Dow Jones Industrial Average", "3M Company (NYSE)", "A.O. Smith Corp (NYSE)", "Abbott Laboratories (NYSE)",
           "AbbVie Inc. (NYSE)", "Accenture plc (NYSE)", "Activision Blizzard (NYSE)", "Acuity Brands Inc (NYSE)",
           "Adobe Systems Inc (NYSE)", "Advance Auto Parts (NYSE)", "Advanced Micro Devices Inc (NYSE)", "AES Corp (NYSE)",
           "Aetna Inc (NYSE)", "Affiliated Managers Group Inc (NYSE)", "AFLAC Inc (NYSE)", "Agilent Technologies Inc (NYSE)",
           "Air Products & Chemicals Inc (NYSE)", "Akamai Technologies Inc (NYSE)", "Alaska Air Group Inc (NYSE)", "Albemarle Corp (NYSE)",
           "Alexandria Real Estate Equities Inc (NYSE)", "Alexion Pharmaceuticals (NYSE)", "Align Technology (NYSE)", "Allegion (NYSE)",
           "Allergan, Plc (NYSE)", "Alliance Data Systems (NYSE)", "Alliant Energy Corp (NYSE)", "Allstate Corp (NYSE)", 
           "Alphabet Inc Class A (NYSE)", "Alphabet Inc Class C (NYSE)", "Altria Group Inc (NYSE)", "Amazon.com Inc (NYSE)", 
           "Ameren Corp (NYSE)", "American Airlines Group (NYSE)", "American Electric Power (NYSE)", "American Express Co (NYSE)", 
           "American International Group, Inc. (NYSE)", "American Tower Corp A (NYSE)", "American Water Works Company Inc (NYSE)",
           "Ameriprise Financial (NYSE)", "AmerisourceBergen Corp (NYSE)", "AMETEK Inc (NYSE)", "Amgen Inc (NYSE)", "Amphenol Corp (NYSE)", 
           "Anadarko Petroleum Corp (NYSE)", "Analog Devices, Inc. (NYSE)", "Andeavor (NYSE)", "ANSYS (NYSE)", "Anthem Inc. (NYSE)", 
           "Aon plc (NYSE)", "Apache Corporation (NYSE)", "Apartment Investment & Management (NYSE)", "Apple Inc. (NYSE)", 
           "Applied Materials Inc (NYSE)", "Aptiv Plc (NYSE)", "Archer-Daniels-Midland Co (NYSE)", "Arconic Inc (NYSE)", 
           "Arthur J. Gallagher & Co. (NYSE)", "Assurant Inc (NYSE)", "AT&T Inc (NYSE)", "Autodesk Inc (NYSE)", "Automatic Data Processing (NYSE)", 
           "AutoZone Inc (NYSE)", "AvalonBay Communities, Inc. (NYSE)", "Avery Dennison Corp (NYSE)", "Baker Hughes, a GE Company (NYSE)", 
           "Ball Corp (NYSE)", "Bank of America Corp (NYSE)", "Baxter International Inc. (NYSE)", "BB&T Corporation (NYSE)", 
           "Becton Dickinson (NYSE)", "Berkshire Hathaway (NYSE)", "Best Buy Co. Inc. (NYSE)", "Biogen Inc. (NYSE)", "BlackRock (NYSE)", 
           "Block H&R (NYSE)", "Boeing Company (NYSE)", "BorgWarner (NYSE)", "Boston Properties (NYSE)", "Boston Scientific (NYSE)", 
           "Brighthouse Financial Inc (NYSE)", "Bristol-Myers Squibb (NYSE)", "Broadcom (NYSE)", "Brown-Forman Corp. (NYSE)", 
           "C. H. Robinson Worldwide (NYSE)", "CA, Inc. (NYSE)", "Cabot Oil & Gas (NYSE)", "Cadence Design Systems (NYSE)", 
           "Campbell Soup (NYSE)", "Capital One Financial (NYSE)", "Cardinal Health Inc. (NYSE)", "Carmax Inc (NYSE)", "Carnival Corp. (NYSE)", 
           "Caterpillar Inc. (NYSE)", "CBOE Holdings (NYSE)", "CBRE Group (NYSE)", "CBS Corp. (NYSE)", "Celgene Corp. (NYSE)", 
           "Centene Corporation (NYSE)", "CenterPoint Energy (NYSE)", "CenturyLink Inc (NYSE)", "Cerner (NYSE)", "CF Industries Holdings Inc (NYSE)", 
           "Charles Schwab Corporation (NYSE)", "Charter Communications (NYSE)", "Chesapeake Energy (NYSE)", "Chevron Corp. (NYSE)", 
           "Chipotle Mexican Grill (NYSE)", "Chubb Limited (NYSE)", "Church & Dwight (NYSE)", "CIGNA Corp. (NYSE)", "Cimarex Energy (NYSE)", 
           "Cincinnati Financial (NYSE)", "Cintas Corporation (NYSE)", "Cisco Systems (NYSE)", "Citigroup Inc. (NYSE)", "Citizens Financial Group (NYSE)", 
           "Citrix Systems (NYSE)", "CME Group Inc. (NYSE)", "CMS Energy (NYSE)", "Coca-Cola Company (The) (NYSE)", "Cognizant Technology Solutions (NYSE)", 
           "Colgate-Palmolive (NYSE)", "Comcast Corp. (NYSE)", "Comerica Inc. (NYSE)", "Conagra Brands (NYSE)", "Concho Resources (NYSE)", 
           "ConocoPhillips (NYSE)", "Consolidated Edison (NYSE)", "Constellation Brands (NYSE)", "Corning Inc. (NYSE)", "Costco Wholesale Corp. (NYSE)", 
           "Coty, Inc (NYSE)", "Crown Castle International Corp. (NYSE)", "CSRA Inc. (NYSE)", "CSX Corp. (NYSE)", "Cummins Inc. (NYSE)", 
           "CVS Health (NYSE)", "D. R. Horton (NYSE)", "Danaher Corp. (NYSE)", "Darden Restaurants (NYSE)", "DaVita Inc. (NYSE)", "Deere & Co. (NYSE)", 
           "Delta Air Lines Inc. (NYSE)", "Dentsply Sirona (NYSE)", "Devon Energy Corp. (NYSE)", "Digital Realty Trust Inc (NYSE)", 
           "Discover Financial Services (NYSE)", "Discovery Communications-A (NYSE)", "Discovery Communications-C (NYSE)", "Dish Network (NYSE)", 
           "Dollar General (NYSE)", "Dollar Tree (NYSE)", "Dominion Energy (NYSE)", "Dover Corp. (NYSE)", "DowDuPont (NYSE)", 
           "Dr Pepper Snapple Group (NYSE)", "DTE Energy Co. (NYSE)", "Duke Energy (NYSE)", "Duke Realty Corp (NYSE)", "DXC Technology (NYSE)", 
           "E*Trade (NYSE)", "Eastman Chemical (NYSE)", "Eaton Corporation (NYSE)", "eBay Inc. (NYSE)", "Ecolab Inc. (NYSE)", "Edison Int'l (NYSE)", 
           "Edwards Lifesciences (NYSE)", "Electronic Arts (NYSE)", "Emerson Electric Company (NYSE)", "Entergy Corp. (NYSE)", "Envision Healthcare (NYSE)", 
           "EOG Resources (NYSE)", "EQT Corporation (NYSE)", "Equifax Inc. (NYSE)", "Equinix (NYSE)", "Equity Residential (NYSE)", 
           "Essex Property Trust, Inc. (NYSE)", "Estee Lauder Cos. (NYSE)", "Everest Re Group Ltd. (NYSE)", "Eversource Energy (NYSE)", "Exelon Corp. (NYSE)", 
           "Expedia Inc. (NYSE)", "Expeditors International (NYSE)", "Express Scripts (NYSE)", "Extra Space Storage (NYSE)", "Exxon Mobil Corp. (NYSE)", 
           "F5 Networks (NYSE)", "Facebook, Inc. (NYSE)", "Fastenal Co (NYSE)", "Federal Realty Investment Trust (NYSE)", "FedEx Corporation (NYSE)", 
           "Fidelity National Information Services (NYSE)", "Fifth Third Bancorp (NYSE)", "FirstEnergy Corp (NYSE)", "Fiserv Inc (NYSE)", 
           "FLIR Systems (NYSE)", "Flowserve Corporation (NYSE)", "Fluor Corp. (NYSE)", "FMC Corporation (NYSE)", "Foot Locker Inc (NYSE)", 
           "Ford Motor (NYSE)", "Fortive Corp (NYSE)", "Fortune Brands Home & Security (NYSE)", "Franklin Resources (NYSE)", "Freeport-McMoRan Inc. (NYSE)", 
           "Gap Inc. (NYSE)", "Garmin Ltd. (NYSE)", "Gartner Inc (NYSE)", "General Dynamics (NYSE)", "General Electric (NYSE)", "General Growth Properties Inc. (NYSE)", 
           "General Mills (NYSE)", "General Motors (NYSE)", "Genuine Parts (NYSE)", "Gilead Sciences (NYSE)", "Global Payments Inc. (NYSE)", 
           "Goldman Sachs Group (NYSE)", "Goodyear Tire & Rubber (NYSE)", "Grainger (W.W.) Inc. (NYSE)", "Halliburton Co. (NYSE)", "Hanesbrands Inc (NYSE)", 
           "Harley-Davidson (NYSE)", "Harris Corporation (NYSE)", "Hartford Financial Svc.Gp. (NYSE)", "Hasbro Inc. (NYSE)", "HCA Holdings (NYSE)", 
           "HCP Inc. (NYSE)", "Helmerich & Payne (NYSE)", "Henry Schein (NYSE)", "Hess Corporation (NYSE)", "Hewlett Packard Enterprise (NYSE)", 
           "Hilton Worldwide Holdings Inc (NYSE)", "Hologic (NYSE)", "Home Depot (NYSE)", "Honeywell Int'l Inc. (NYSE)", "Hormel Foods Corp. (NYSE)", 
           "Host Hotels & Resorts (NYSE)", "HP Inc. (NYSE)", "Humana Inc. (NYSE)", "Huntington Bancshares (NYSE)", "Huntington Ingalls Industries (NYSE)", 
           "IDEX Laboratories (NYSE)", "IDEXX Laboratories (NASDAQ)", "IHS Markit Ltd. (NYSE)", "Illinois Tool Works (NYSE)", "Illumina Inc (NASDAQ)", 
           "Incyte (NASDAQ)", "Ingersoll-Rand PLC (NYSE)", "Ingredion (NYSE)", "Insight Enterprises (NASDAQ)", "Intel Corp (NASDAQ)", 
           "Intercontinental Exchange (NYSE)", "International Business Machines (NYSE)", "International Paper (NYSE)", "Interpublic Group (NYSE)", 
           "Intuit Inc (NASDAQ)", "Intuitive Surgical (NASDAQ)", "Invesco Ltd. (NYSE)", "IPG Photonics Corp (NASDAQ)", "IQVIA Holdings Inc (NYSE)", 
           "Iron Mountain Incorporated (NYSE)", "J. B. Hunt Transport Services (NASDAQ)", "J. M. Smucker (NYSE)", "Jack Henry & Associates (NASDAQ)", 
           "Jacobs Engineering Group (NYSE)", "Jazz Pharmaceuticals (NASDAQ)", "JetBlue Airways (NASDAQ)", "Johnson & Johnson (NYSE)", "Johnson Controls International plc (NYSE)", 
           "Juniper Networks (NYSE)", "Kansas City Southern (NYSE)", "Kellogg Co (NYSE)", "KeyCorp (NYSE)", "Keysight Technologies (NYSE)", 
           "Kimberly-Clark (NYSE)", "Kimco Realty (NYSE)", "Kinder Morgan (NYSE)", "KLA Corporation (NASDAQ)", "Kohl's Corp. (NYSE)", 
           "Kraft Heinz Co (NASDAQ)", "Kroger Co. (NYSE)", "L Brands Inc. (NYSE)", "L3 Technologies (NYSE)", "Laboratory Corp. of America Holding (NYSE)", 
           "Lam Research (NASDAQ)", "Lamb Weston Holdings Inc (NYSE)", "Las Vegas Sands (NYSE)", "Leggett & Platt (NYSE)", "Leidos Holdings (NYSE)", 
           "Lennar Corp. (NYSE)", "Lilly (Eli) & Co (NYSE)", "Lincoln National (NYSE)", "Linde plc (NYSE)", "Live Nation Entertainment (NYSE)", 
           "LKQ Corporation (NASDAQ)", "Lockheed Martin Corp. (NYSE)", "Loews Corp. (NYSE)", "Lowe's Cos. (NYSE)", "LyondellBasell (NYSE)", 
           "M&T Bank Corp. (NYSE)", "Macerich (NYSE)", "Macy's Inc. (NYSE)", "Magellan Midstream Partners L.P. (NYSE)", "ManpowerGroup (NYSE)", 
           "Marathon Oil Corp. (NYSE)", "Marathon Petroleum (NYSE)", "Markel Corp. (NYSE)", "Marriott Int'l. (NASDAQ)", "Marsh & McLennan (NYSE)", 
           "Martin Marietta Materials (NYSE)", "Masco Corp. (NYSE)", "Mastercard Inc. (NYSE)", "Mattel Inc. (NASDAQ)", "McCormick & Co. (NYSE)", 
           "McDonald's Corp. (NYSE)", "McKesson Corp. (NYSE)", "Medtronic plc (NYSE)", "Merck & Co. (NYSE)", "MetLife Inc. (NYSE)", 
           "Mettler Toledo (NYSE)", "MGM Resorts International (NYSE)", "Microchip Technology (NASDAQ)", "Micron Technology (NASDAQ)", "Microsoft Corp. (NASDAQ)", 
           "Mid-America Apartments (NYSE)", "Mohawk Industries (NYSE)", "Molson Coors Brewing Company (NYSE)", "Mondelez International (NASDAQ)", "Monster Beverage (NASDAQ)", 
           "Moody's Corp (NYSE)", "Morgan Stanley (NYSE)", "Motorola Solutions Inc. (NYSE)", "MSCI Inc (NYSE)", "Mylan N.V. (NASDAQ)", 
           "Nasdaq, Inc. (NASDAQ)", "National Oilwell Varco Inc. (NYSE)", "NetApp (NASDAQ)", "Netflix Inc. (NASDAQ)", "Newell Brands (NASDAQ)", 
           "Newmont Mining Corporation (NYSE)", "News Corp. Class A (NASDAQ)", "News Corp. Class B (NASDAQ)", "NextEra Energy (NYSE)", "Nielsen Holdings (NYSE)", 
           "Nike (NYSE)", "NiSource Inc. (NYSE)", "Noble Energy Inc. (NYSE)", "Nordstrom (NYSE)", "Norfolk Southern Corp. (NYSE)", 
           "Northern Trust Corp. (NASDAQ)", "Northrop Grumman (NYSE)", "Norwegian Cruise Line Holdings (NYSE)", "NRG Energy (NYSE)", "Nucor Corp. (NYSE)", 
           "NVIDIA Corporation (NASDAQ)", "O'Reilly Automotive (NASDAQ)", "Occidental Petroleum (NYSE)", "Omnicom Group (NYSE)", "ONEOK (NYSE)", 
           "Oracle Corp. (NYSE)", "PACCAR Inc. (NASDAQ)", "Packaging Corporation of America (NYSE)", "Parker-Hannifin (NYSE)", "Paychex Inc. (NASDAQ)", 
           "PayPal (NASDAQ)", "Pentair plc (NYSE)", "PepsiCo Inc. (NASDAQ)", "PerkinElmer (NYSE)", "Perrigo (NYSE)", 
           "Pfizer Inc. (NYSE)", "Philip Morris International (NYSE)", "Phillips 66 (NYSE)", "Pinnacle West Capital (NYSE)", "Pioneer Natural Resources (NYSE)", 
           "Pitney Bowes (NYSE)", "PNC Financial Services (NYSE)", "Polo Ralph Lauren Corp. (NYSE)", "PPG Industries (NYSE)", "PPL Corp. (NYSE)", 
           "Principal Financial Group (NYSE)", "Procter & Gamble (NYSE)", "Progressive Corp. (NYSE)", "Prologis (NYSE)", "Prudential Financial (NYSE)", 
           "Public Serv. Enterprise Inc. (NYSE)", "Public Storage (NYSE)", "Pulte Homes Inc. (NYSE)", "PVH Corp. (NYSE)", "Qorvo (NASDAQ)", 
           "QUALCOMM Inc. (NASDAQ)", "Quanta Services Inc. (NYSE)", "Quest Diagnostics (NYSE)", "Ralph Lauren Corporation (NYSE)", "Raymond James Financial Inc. (NYSE)", 
           "Raytheon Co. (NYSE)", "Realty Income Corporation (NYSE)", "Regency Centers Corporation (NYSE)", "Regeneron (NASDAQ)", "Regions Financial Corp. (NYSE)", 
           "Republic Services Inc. (NYSE)", "ResMed (NYSE)", "Robert Half International (NYSE)", "Rockwell Automation Inc. (NYSE)", "Rockwell Collins (NYSE)", 
           "Rollins Inc. (NYSE)", "Roper Technologies (NYSE)", "Ross Stores (NASDAQ)", "Royal Caribbean Cruises Ltd (NYSE)", "Royal Gold Inc. (NASDAQ)", 
           "S&P Global, Inc. (NYSE)", "Salesforce.com (NYSE)", "SBA Communications (NASDAQ)", "Schlumberger Ltd. (NYSE)", "Schwab (NYSE)", 
           "Seagate Technology (NASDAQ)", "Sealed Air (NYSE)", "Sempra Energy (NYSE)", "Sherwin-Williams (NYSE)", "Simon Property Group Inc (NYSE)", 
           "Skyworks Solutions (NASDAQ)", "SL Green Realty (NYSE)", "Snap-on (NYSE)", "Southern Co. (NYSE)", "Southwest Airlines (NYSE)", 
           "Stanley Black & Decker (NYSE)", "Starbucks Corp. (NASDAQ)", "State Street Corp. (NYSE)", "Stericycle Inc (NASDAQ)", "Stryker Corp. (NYSE)", 
           "SunTrust Banks (NYSE)", "Symantec Corp. (NASDAQ)", "Synchrony Financial (NYSE)", "Synopsys Inc. (NASDAQ)", "Sysco Corp. (NYSE)", 
           "T-Mobile US (NASDAQ)", "T. Rowe Price Group (NASDAQ)", "Take-Two Interactive (NASDAQ)", "Tapestry, Inc. (NYSE)", "Target Corp. (NYSE)", 
           "TE Connectivity Ltd. (NYSE)", "TechnipFMC (NYSE)", "Teleflex Inc. (NYSE)", "Texas Instruments (NASDAQ)", "Textron Inc. (NYSE)", 
           "Thermo Fisher Scientific (NYSE)", "Tiffany & Co. (NYSE)", "Time Warner (NYSE)", "TJX Companies Inc. (NYSE)", "Torchmark Corp. (NYSE)", 
           "Total System Services (NYSE)", "Tractor Supply Company (NASDAQ)", "TransDigm Group (NYSE)", "Transocean (NYSE)", "TripAdvisor (NASDAQ)", 
           "Twenty-First Century Fox Class A (NASDAQ)", "Twenty-First Century Fox Class B (NASDAQ)", "Tyson Foods (NYSE)", "UDR Inc. (NYSE)", "Ulta Beauty (NASDAQ)", 
           "Umpqua Holdings Corp (NASDAQ)", "Under Armour (NYSE)", "Union Pacific (NYSE)", "United Continental Holdings (NASDAQ)", "United Health Group Inc. (NYSE)", 
           "United Parcel Service (NYSE)", "United Rentals, Inc. (NYSE)", "United Technologies (NYSE)", "Universal Health Services (NYSE)", "Unum Group (NYSE)", 
           "Valero Energy (NYSE)", "Varian Medical Systems (NYSE)", "Ventas Inc (NYSE)", "Verisign Inc. (NASDAQ)", "Verisk Analytics (NASDAQ)", 
           "Verizon Communications (NYSE)", "Vertex Pharmaceuticals Inc (NASDAQ)", "VF Corp. (NYSE)", "Viacom Inc. (NASDAQ)", "Visa Inc. (NYSE)", 
           "Vornado Realty Trust (NYSE)", "Vulcan Materials (NYSE)", "Walgreens Boots Alliance (NASDAQ)", "Walmart (NYSE)", "Walt Disney (NYSE)", 
           "Waste Management Inc. (NYSE)", "Waters Corporation (NYSE)", "Wec Energy Group Inc (NYSE)", "WellCare Health Plans (NYSE)", "Wells Fargo (NYSE)", 
           "Welltower Inc. (NYSE)", "Western Digital (NASDAQ)", "Western Union Co (NYSE)", "WestRock (NYSE)", "Weyerhaeuser Corp. (NYSE)", 
           "Whirlpool Corp. (NYSE)", "Williams Companies (NYSE)", "Willis Towers Watson (NASDAQ)", "Wynn Resorts Ltd (NASDAQ)", "Xcel Energy Inc. (NASDAQ)", 
           "Xerox Corp. (NYSE)", "Xilinx Inc (NASDAQ)", "Xylem Inc. (NYSE)", "Yum! Brands Inc (NYSE)", "Zimmer Biomet Holdings (NYSE)", 
           "Zions Bancorp (NASDAQ)", "Zoetis Inc. (NYSE)")

code = ("", "^NSEI", "^DJI", "MMM", "AOS", "ABT", "ABBV", "ACN", "ATVI", "AYI", "ADBE", "AAP", "AMD", "AES", "AET", "AMG", "AFL", 
        "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALXN", "ALGN", "ALLE", "AGN", "ADS", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", 
        "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI", "ANDV", "ANSS", "ANTM", "AON", 
        "APA", "AIV", "AAPL", "AMAT", "APTV", "ADM", "ARNC", "AJG", "AIZ", "T", "ADSK", "ADP", "AZO", "AVB", "AVY", "BHGE", "BLL", 
        "BAC", "BAX", "BRK.B", "BBY", "BIIB", "BLK", "HRB", "BA", "BWA", "BXP", "BSX", "BHF", "BMY", "AVGO", "BF.B", "CHRW", "CA", 
        "COG", "CDNS", "CPB", "COF", "CAH", "KMX", "CCL", "CAT", "CBOE", "CBRE", "CBS", "CELG", "CNC", "CNP", "CTL", "CERN", "CF", 
        "SCHW", "CHTR", "CHK", "CVX", "CMG", "CB", "CHD", "CI", "XEC", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CME", "CMS", 
        "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "ED", "STZ", "GLW", "COST", "COTY", "CCI", "CSRA", "CSX", "CMI", 
        "CVS", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", "D", 
        "DOV", "DWDP", "DPS", "DTE", "DUK", "DRE", "DXC", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "EMR", "ETR", 
        "EVHC", "EOG", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "RE", "ES", "EXC", "EXPE", "EXPD", "ESRX", "EXR", "XOM", "FFIV", 
        "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FISV", "FLIR", "FLS", "FLR", "FMC", "FL", "F", "FTV", "FBHS", "BEN", 
        "FCX", "GPS", "GRMN", "IT", "GD", "GE", "GGP", "GIS", "GM", "GPC", "GILD", "GPN", "GS", "GT", "GWW", "HAL", "HBI", "HOG", 
        "HRS", "HIG", "HAS", "HCA", "HCP", "HP", "HSIC", "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HPQ", "HUM", 
        "HBAN", "HII", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR", "INGR", "NSIT", "INTC", "ICE", "IBM", "IP", "IPG", "INTU", 
        "ISRG", "IVZ", "IPGP", "IQV", "IRM", "JBHT", "SJM", "JKHY", "JEC", "JAZZ", "JBLU", "JNJ", "JCI", "JNPR", "KSU", "K", 
        "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KSS", "KHC", "KR", "LB", "LLL", "LH", "LIN", "LYV", "LKQ", "LMT", "L", 
        "LOW", "LYB", "MTB", "MAC", "M", "MMP", "MAN", "MRO", "MPC", "MKL", "MAR", "MMC", "MLM", "MAS", "MA", "MAT", "MKC", 
        "MCD", "MCK", "MDT", "MRK", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MHK", "TAP", "MDLZ", "MNST", "MCO", 
        "MS", "MSI", "MSCI", "MYL", "NDAQ", "NOV", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", 
        "NBL", "JWN", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "ORLY", "OXY", "OMC", "OKE", "ORCL", "PCAR", "PKG", "PH", 
        "PAYX", "PYPL", "PNR", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX", "PNW", "PXD", "PBI", "PNC", "RL", "PPG", "PPL", 
        "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "QRVO", "QCOM", "PWR", "DGX", "RL", "RJF", "RTN", 
        "O", "REG", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "COL", "ROL", "ROP", "ROST", "RCL", "RGLD", "SPGI", 
        "CRM", "SBAC", "SLB", "SCHW", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SIRI", "SO", "LUV", "SWK", "SBUX", "STT", 
        "SRCL", "SYK", "STI", "SYMC", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TGT", "TEL", "FTI", "TFX", 
        "TXN", "TXT", "TMO", "TIF", "TWX", "TJX", "TMK", "TSS", "TSCO", "TDG", "RIG", "TRIP", "FOXA", "FOX", "TSN", "UDR", 
        "ULTA", "UMPQ", "UAA", "UNP", "UAL", "UNH", "UPS", "URI", "UTX", "UHS", "UNM", "VLO", "VAR", "VTR", "VRSN", "VRSK", 
        "VZ", "VRTX", "VFC", "VIAB", "V", "VNO", "VMC", "WBA", "WMT", "DIS", "WM", "WAT", "WEC", "WCG", "WFC", "WELL", 
        "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XEL", "XRX", "XLNX", "XYL", "YUM", "ZBH", "ZION", "ZTS", 
        "AAPL", "AMZN", "GOOGL", "FB", "JNJ", "BABA", "V", "JPM", "TSM", "WMT", "MSFT", "PG", "PYPL", "NVDA", "HD", "DIS", 
        "UNH", "VZ", "INTC", "MA", "ADBE", "NFLX", "CMCSA", "PEP", "CSCO", "NKE", "XOM", "ABT", "ABBV", "ACN", "ATVI", "AYI", 
        "ADBE", "AAP", "AMD", "AES", "AET", "AMG", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALXN", "ALGN", "ALLE", 
        "AGN", "ADS", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", 
        "ABC", "AME", "AMGN", "APH", "ADI", "ANDV", "ANSS", "ANTM", "AON", "APA", "AIV", "AAPL", "AMAT", "APTV", "ADM", 
        "ARNC", "AJG", "AIZ", "T", "ADSK", "ADP", "AZO", "AVB", "AVY", "BHGE", "BLL", "BAC", "BAX", "BRK.B", "BBY", "BIIB", 
        "BLK", "HRB", "BA", "BWA", "BXP", "BSX", "BHF", "BMY", "AVGO", "BF.B", "CHRW", "CA", "COG", "CDNS", "CPB", "COF", 
        "CAH", "KMX", "CCL", "CAT", "CBOE", "CBRE", "CBS", "CELG", "CNC", "CNP", "CTL", "CERN", "CF", "SCHW", "CHTR", "CHK", 
        "CVX", "CMG", "CB", "CHD", "CI", "XEC", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CME", "CMS", "KO", "CTSH", 
        "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "ED", "STZ", "GLW", "COST", "COTY", "CCI", "CSRA", "CSX", "CMI", "CVS", 
        "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", "D", 
        "DOV", "DWDP", "DPS", "DTE", "DUK", "DRE", "DXC", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "EMR", 
        "ETR", "EVHC", "EOG", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "RE", "ES", "EXC", "EXPE", "EXPD", "ESRX", "EXR", 
        "XOM", "FFIV", "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FISV", "FLIR", "FLS", "FLR", "FMC", "FL", "F", 
        "FTV", "FBHS", "BEN", "FCX", "GPS", "GRMN", "IT", "GD", "GE", "GGP", "GIS", "GM", "GPC", "GILD", "GPN", "GS", 
        "GT", "GWW", "HAL", "HBI", "HOG", "HRS", "HIG", "HAS", "HCA", "HCP", "HP", "HSIC", "HES", "HPE", "HLT", "HOLX", 
        "HD", "HON", "HRL", "HST", "HPQ", "HUM", "HBAN", "HII", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR", "INGR", "NSIT", 
        "INTC", "ICE", "IBM", "IP", "IPG", "INTU", "ISRG", "IVZ", "IPGP", "IQV", "IRM", "JBHT", "SJM", "JKHY", "JEC", "JAZZ", 
        "JBLU", "JNJ", "JCI", "JNPR", "KSU", "K", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KSS", "KHC", "KR", "LB", 
        "LLL", "LH", "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LYB", "MTB", "MAC", "M", "MMP", "MAN", "MRO", "MPC", "MKL", 
        "MAR", "MMC", "MLM", "MAS", "MA", "MAT", "MKC", "MCD", "MCK", "MDT", "MRK", "MET", "MTD", "MGM", "MCHP", "MU", 
        "MSFT", "MAA", "MHK", "TAP", "MDLZ", "MNST", "MCO", "MS", "MSI", "MSCI", "MYL", "NDAQ", "NOV", "NTAP", "NFLX", "NWL", 
        "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "JWN", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "ORLY", 
        "OXY", "OMC", "OKE", "ORCL", "PCAR", "PKG", "PH", "PAYX", "PYPL", "PNR", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX", 
        "PNW", "PXD", "PBI", "PNC", "RL", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "QRVO", 
        "QCOM", "PWR", "DGX", "RL", "RJF", "RTN", "O", "REG", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "COL", "ROL", 
        "ROP", "ROST", "RCL", "RGLD", "SPGI", "CRM", "SBAC", "SLB", "SCHW", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SIRI", 
        "SO", "LUV", "SWK", "SBUX", "STT", "SRCL", "SYK", "STI", "SYMC", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", 
        "TGT", "TEL", "FTI", "TFX", "TXN", "TXT", "TMO", "TIF", "TWX", "TJX", "TMK", "TSS", "TSCO", "TDG", "RIG", "TRIP", "FOXA", 
        "FOX", "TSN", "UDR", "ULTA", "UMPQ", "UAA", "UNP", "UAL", "UNH", "UPS", "URI", "UTX", "UHS", "UNM", "VLO", "VAR", "VTR", 
        "VRSN", "VRSK", "VZ", "VRTX", "VFC", "VIAB", "V", "VNO", "VMC", "WBA", "WMT", "DIS", "WM", "WAT", "WEC", "WCG", "WFC", 
        "WELL", "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XEL", "XRX", "XLNX", "XYL", "YUM", "ZBH", "ZION", 
        "ZTS", "AAPL", "AMZN", "GOOGL", "FB", "JNJ", "BABA", "V", "JPM", "TSM", "WMT", "MSFT", "PG", "PYPL", "NVDA", "HD", 
        "DIS", "UNH", "VZ", "INTC", "MA", "ADBE", "NFLX", "CMCSA", "PEP", "CSCO", "NKE", "XOM", "ABT", "ABBV", "ACN", "ATVI", 
        "AYI", "ADBE", "AAP", "AMD", "AES", "AET", "AMG", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALXN", "ALGN", 
        "ALLE", "AGN", "ADS", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", 
        "AMP", "ABC", "AME", "AMGN", "APH", "ADI", "ANDV", "ANSS", "ANTM", "AON", "APA", "AIV", "AAPL", "AMAT", "APTV", 
        "ADM", "ARNC", "AJG", "AIZ", "T", "ADSK", "ADP", "AZO", "AVB", "AVY", "BHGE", "BLL", "BAC", "BAX", "BRK.B", "BBY", 
        "BIIB", "BLK", "HRB", "BA", "BWA", "BXP", "BSX", "BHF", "BMY", "AVGO", "BF.B", "CHRW", "CA", "COG", "CDNS", "CPB", 
        "COF", "CAH", "KMX", "CCL", "CAT", "CBOE", "CBRE", "CBS", "CELG", "CNC", "CNP", "CTL", "CERN", "CF", "SCHW", "CHTR", 
        "CHK", "CVX", "CMG", "CB", "CHD", "CI", "XEC", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CME", "CMS", "KO", 
        "CTSH", "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "ED", "STZ", "GLW", "COST", "COTY", "CCI", "CSRA", "CSX", "CMI", 
        "CVS", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", 
        "D", "DOV", "DWDP", "DPS", "DTE", "DUK", "DRE", "DXC", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", 
        "EMR", "ETR", "EVHC", "EOG", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "RE", "ES", "EXC", "EXPE", "EXPD", "ESRX", 
        "EXR", "XOM", "FFIV", "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FISV", "FLIR", "FLS", "FLR", "FMC", "FL", 
        "F", "FTV", "FBHS", "BEN", "FCX", "GPS", "GRMN", "IT", "GD", "GE", "GGP", "GIS", "GM", "GPC", "GILD", "GPN", 
        "GS", "GT", "GWW", "HAL", "HBI", "HOG", "HRS", "HIG", "HAS", "HCA", "HCP", "HP", "HSIC", "HES", "HPE", "HLT", 
        "HOLX", "HD", "HON", "HRL", "HST", "HPQ", "HUM", "HBAN", "HII", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR", 
        "INGR", "NSIT", "INTC", "ICE", "IBM", "IP", "IPG", "INTU", "ISRG", "IVZ", "IPGP", "IQV", "IRM", "JBHT", "SJM", 
        "JKHY", "JEC", "JAZZ", "JBLU", "JNJ", "JCI", "JNPR", "KSU", "K", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", 
        "KSS", "KHC", "KR", "LB", "LLL", "LH", "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LYB", "MTB", "MAC", "M", 
        "MMP", "MAN", "MRO", "MPC", "MKL", "MAR", "MMC", "MLM", "MAS", "MA", "MAT", "MKC", "MCD", "MCK", "MDT", "MRK", 
        "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MHK", "TAP", "MDLZ", "MNST", "MCO", "MS", "MSI", "MSCI", 
        "MYL", "NDAQ", "NOV", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "JWN", 
        "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "ORLY", "OXY", "OMC", "OKE", "ORCL", "PCAR", "PKG", "PH", "PAYX", 
        "PYPL", "PNR", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX", "PNW", "PXD", "PBI", "PNC", "RL", "PPG", "PPL", "PFG", 
        "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "QRVO", "QCOM", "PWR", "DGX", "RL", "RJF", "RTN", "O", 
        "REG", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "COL", "ROL", "ROP", "ROST", "RCL", "RGLD", "SPGI", 
        "CRM", "SBAC", "SLB", "SCHW", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SIRI", "SO", "LUV", "SWK", "SBUX", 
        "STT", "SRCL", "SYK", "STI", "SYMC", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TGT", "TEL", "FTI", 
        "TFX", "TXN", "TXT", "TMO", "TIF", "TWX", "TJX", "TMK", "TSS", "TSCO", "TDG", "RIG", "TRIP", "FOXA", "FOX", 
        "TSN", "UDR", "ULTA", "UMPQ", "UAA", "UNP", "UAL", "UNH", "UPS", "URI", "UTX", "UHS", "UNM", "VLO", "VAR", "VTR", 
        "VRSN", "VRSK", "VZ", "VRTX", "VFC", "VIAB", "V", "VNO", "VMC", "WBA", "WMT", "DIS", "WM", "WAT", "WEC", "WCG", 
        "WFC", "WELL", "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XEL", "XRX", "XLNX", "XYL", "YUM", "ZBH", 
        "ZION", "ZTS", "AAPL", "AMZN", "GOOGL", "FB", "JNJ", "BABA", "V", "JPM", "TSM", "WMT", "MSFT", "PG", "PYPL", "NVDA", 
        "HD", "DIS", "UNH", "VZ", "INTC", "MA", "ADBE", "NFLX", "CMCSA", "PEP", "CSCO", "NKE", "XOM", "ABT", "ABBV", "ACN", 
        "ATVI", "AYI", "ADBE", "AAP", "AMD", "AES", "AET", "AMG", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALXN", 
        "ALGN", "ALLE", "AGN", "ADS", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AEE", "AAL", "AEP", "AXP", "AIG", 
        "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI", "ANDV", "ANSS", "ANTM", "AON", "APA", "AIV", "AAPL", 
        "AMAT", "APTV", "ADM", "ARNC", "AJG", "AIZ", "T", "ADSK", "ADP", "AZO", "AVB", "AVY", "BHGE", "BLL", "BAC", "BAX", 
        "BRK.B", "BBY", "BIIB", "BLK", "HRB", "BA", "BWA", "BXP", "BSX", "BHF", "BMY", "AVGO", "BF.B", "CHRW", "CA", 
        "COG", "CDNS", "CPB", "COF", "CAH", "KMX", "CCL", "CAT", "CBOE", "CBRE", "CBS", "CELG", "CNC", "CNP", "CTL", 
        "CERN", "CF", "SCHW", "CHTR", "CHK", "CVX", "CMG", "CB", "CHD", "CI", "XEC", "CINF", "CTAS", "CSCO", "C", 
        "CFG", "CTXS", "CME", "CMS", "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "ED", "STZ", "GLW", 
        "COST", "COTY", "CCI", "CSRA", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", 
        "DLR", "DFS", "DISCA", "DISCK", "DISH", "DG", "DLTR", "D", "DOV", "DWDP", "DPS", "DTE", "DUK", "DRE", "DXC", 
        "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "EMR", "ETR", "EVHC", "EOG", "EQT", "EFX", "EQIX", 
        "EQR", "ESS", "EL", "RE", "ES", "EXC", "EXPE", "EXPD", "ESRX", "EXR", "XOM", "FFIV", "FB", "FAST", "FRT", 
        "FDX", "FIS", "FITB", "FE", "FISV", "FLIR", "FLS", "FLR", "FMC", "FL", "F", "FTV", "FBHS", "BEN", "FCX", 
        "GPS", "GRMN", "IT", "GD", "GE", "GGP", "GIS", "GM", "GPC", "GILD", "GPN", "GS", "GT", "GWW", "HAL", 
        "HBI", "HOG", "HRS", "HIG", "HAS", "HCA", "HCP", "HP", "HSIC", "HES", "HPE", "HLT", "HOLX", "HD", "HON", 
        "HRL", "HST", "HPQ", "HUM", "HBAN", "HII", "IDXX", "INFO", "ITW", "ILMN", "INCY", "IR", "INGR", "NSIT", "INTC", 
        "ICE", "IBM", "IP", "IPG", "INTU", "ISRG", "IVZ", "IPGP", "IQV", "IRM", "JBHT", "SJM", "JKHY", "JEC", "JAZZ", 
        "JBLU", "JNJ", "JCI", "JNPR", "KSU", "K", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KSS", "KHC", "KR", 
        "LB", "LLL", "LH", "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LYB", "MTB", "MAC", "M", "MMP", "MAN", 
        "MRO", "MPC", "MKL", "MAR", "MMC", "MLM", "MAS", "MA", "MAT", "MKC", "MCD", "MCK", "MDT", "MRK", "MET", 
        "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MHK", "TAP", "MDLZ", "MNST", "MCO", "MS", "MSI", "MSCI", "MYL", 
        "NDAQ", "NOV", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "JWN", "NTRS", 
        "NOC", "NCLH", "NRG", "NUE", "NVDA", "ORLY", "OXY", "OMC", "OKE", "ORCL", "PCAR", "PKG", "PH", "PAYX", "PYPL", 
        "PNR", "PEP", "PKI", "PRGO", "PFE", "PM", "PSX", "PNW", "PXD", "PBI", "PNC", "RL", "PPG", "PPL", "PFG", 
        "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "QRVO", "QCOM", "PWR", "DGX", "RL", "RJF", "RTN", 
        "O", "REG", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "COL", "ROL", "ROP", "ROST", "RCL", "RGLD", 
        "SPGI", "CRM", "SBAC", "SLB", "SCHW", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SIRI", "SO", "LUV", "SWK", 
        "SBUX", "STT", "SRCL", "SYK", "STI", "SYMC", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TGT", "TEL", 
        "FTI", "TFX", "TXN", "TXT", "TMO", "TIF", "TWX", "TJX", "TMK", "TSS", "TSCO", "TDG", "RIG", "TRIP", "FOXA", 
        "FOX", "TSN", "UDR", "ULTA", "UMPQ", "UAA", "UNP", "UAL", "UNH", "UPS", "URI", "UTX", "UHS", "UNM", "VLO", 
        "VAR", "VTR", "VRSN", "VRSK", "VZ", "VRTX", "VFC", "VIAB", "V", "VNO", "VMC", "WBA", "WMT", "DIS", "WM", 
        "WAT", "WEC", "WCG", "WFC", "WELL", "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XEL", "XRX", 
        "XLNX", "XYL", "YUM", "ZBH", "ZION", "ZTS")

nifty = yf.Ticker('^DJI')
currentN = nifty.history(period='5d')['Close'].iloc[-1]
lastN = nifty.history(period='5d')['Close'].iloc[-2]
changeN = currentN - lastN
percentage_changeN = (changeN / lastN) * 100
current_formattedN = f"{currentN:.2f}"
change_formattedN = f"{changeN:.2f}"
percentage_change_formattedN = f"{percentage_changeN:.2f}%"

# sensex = yf.Ticker('^BSESN')
# currentS = sensex.history(period='5d')['Close'].iloc[-1]
# lastS = sensex.history(period='5d')['Close'].iloc[-2]
# changeS = currentS - lastS
# percentage_changeS = (changeS / lastS) * 100
# current_formattedS = f"${currentS:.2f}"
# change_formattedS = f"{changeS:.2f}"
# percentage_change_formattedS = f"{percentage_changeS:.2f}%"

if not selected == "HELP":
    selected_company = st.selectbox("\n\nSearch for a Company", company)
    st.write("---")
    n = company.index(selected_company)
    selected_stocks = code[n]
    
    
    if selected == "HOME":
        
            col1,col2=st.columns(2)
            with col1:
                st.subheader("Dow Jones Industrial Average")
                st.metric(label="", value=current_formattedN, delta=f"{change_formattedN} ({percentage_change_formattedN})")
            # with col3:
            #     st.subheader("Sensex")
            #     st.metric(label="", value=current_formattedS, delta=f"{change_formattedS} ({percentage_change_formattedS})")
            # st.write("---")      
       
        
    if selected_stocks:
        if n>0:
            st.subheader(f" {company[n]} ({code[n]})") 
            st.write("---")
        data = yf.download(tickers=selected_stocks, start="2015-01-01", end=date.today().strftime("%Y-%m-%d"))
        T = yf.Ticker(selected_stocks)
        if selected == "HOME":
            
            current = T.history(period='5d')['Close'].iloc[-1]
            last = T.history(period='5d')['Close'].iloc[-2]
            change = current - last
            percentage_change = (change / last) * 100
            current_formatted = f"${current:.2f}"
            change_formatted = f"{change:.2f}"
            percentage_change_formatted = f"{percentage_change:.2f}%"
            st.metric(label=T.info['longName'], value=current_formatted, delta=f"{change_formatted} ({percentage_change_formatted})")

            if change > 0:
                graphColour = 'green'
            else:
                graphColour = 'red'
            data_reset = data.reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_reset['Date'], y=data_reset['Adj Close'], name="Prices", line=dict(color=graphColour)))
            fig.layout.update(title_text="Prices", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
            st.write("---")
                
            close = T.info['previousClose']
            opening = T.info['open']
            h = T.info['dayHigh']
            l = T.info['dayLow']
            Fhigh = T.info['fiftyTwoWeekHigh']
            Flow = T.info['fiftyTwoWeekLow']
            v = T.info['volume']
            
            col1,col2=st.columns(2)
            with col1:
                st.write(f'**Opening Price** = $ {round(opening, 2)}')
                st.write(f'**Closing Price** = $ {round(close, 2)}')
            with col2:
                st.write(f'**Days Range** = $ {round(l, 2)} - $ {round(h, 2)}')
                st.write(f'**Volume** = {v}')
            st.write(f' **52 Week Low - High** = $ {round(Flow,2)} - $ {round(Fhigh,2)}')          
                
            today = datetime.today()
            start_date = today - timedelta(days=7)
            
            col1,col2=st.columns(2)
            data1 = yf.download(tickers=selected_stocks, start=start_date, end=today)
            
            data1.index = pd.to_datetime(data1.index).tz_localize('UTC').tz_convert('Asia/Kolkata')
                        
            data1.index = data1.index.strftime('%d-%m-%Y')
            rounded_data = {col: data1[col].round(2) for col in data1.columns if data1[col].dtype != 'object'}
            data_rounded = pd.DataFrame(rounded_data)
            st.write("---")
            st.subheader("Data Chart")
            st.dataframe(data_rounded)
        
        if selected == "LIVE PRICES":
            st.header("Live Price Updates")
            st.write("Updates only in Market Hours")
            col1,col2,col3=st.columns(3)
            with col1:
                live_button = st.button("Live Prices")

            if live_button:
                metric_placeholder = st.empty()
                with col2:
                    exit_button = st.button("Exit")
                exit_clicked = False 

                while not exit_clicked:
                    current = T.history(period='5d')['Close'].iloc[-1]
                    last = T.history(period='5d')['Close'].iloc[-2]
                    change = current - last
                    percentage_change = (change / last) * 100
                    current_formatted = f"${current:.2f}"
                    change_formatted = f"{change:.2f}"
                    percentage_change_formatted = f"{percentage_change:.2f}%"

                    metric_placeholder.subheader("Nifty 50")
                    metric_placeholder.metric(label="Live Prices", value=current_formatted, delta=f"{change_formatted} ({percentage_change_formatted})")

                    if exit_button:
                        exit_clicked = True  
                    time.sleep(0.25)
            st.write("---")
    
        if selected == "GRAPHS":
            
            st.header("GRAPHS")
            st.write("---")
            st.write("You can select time period of data ")
            col1,col2=st.columns(2)
            with col1:
                START = st.date_input('Enter start date', value=pd.to_datetime('2020-01-01'))
            with col2:
                END = st.date_input('Enter end date', value=pd.to_datetime(date.today().strftime("%Y-%m-%d")))
            
            d= yf.download(tickers=selected_stocks, start=START, end=END).reset_index()
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=d['Date'], y=d['Open'], name="Opening Price"))  
            fig1.add_trace(go.Scatter(x=d['Date'], y=d['Close'], name="Closing Price"))
            fig1.layout.update(title_text="Opening and Closing Prices", xaxis_rangeslider_visible=True)
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=d['Date'], y=d['High'], name="High"))  
            fig2.add_trace(go.Scatter(x=d['Date'], y=d['Low'], name="Low"))
            fig2.layout.update(title_text="Low and High Prices", xaxis_rangeslider_visible=True)
            
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=d['Date'], y=d['Volume'], name="Volume"))
            fig3.layout.update(title_text="Volume", xaxis_rangeslider_visible=True)
            
            st.write("Click to preview Graph")
            col4,col5,col6=st.columns(3)
            with col4:
               button3=st.button("Opening and Closing Prices")
            with col5:
               button4=st.button("Low and High")
            with col6:
                button5=st.button("Volume")
        
            if button3:
                st.write("Prices v/s Time")
                st.plotly_chart(fig1)  
                st.button("Exit  ")
            
            if button4:
                st.write("Prices v/s Time")
                
                st.plotly_chart(fig2)
                st.button("Exit     ")
            if button5:
                st.write("Volumes v/s Time")
                st.plotly_chart(fig3)
                st.button("Exit      ")
        
        if selected == "DATA":
            
            st.write("See Data in a Time Interval")
            col1, col2, col3 = st.columns(3)
            t = ["1m", "5m", "15m", "30m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
            
            today = datetime.today().date()
            start_date = (today - timedelta(days=7))
            
            with col3:
                selected_interval = st.selectbox("Select a Time Interval", t)
            with col1:
                start = st.date_input('Enter start date', value=start_date)
            with col2:
                end = st.date_input('Enter end date', value=today)
            
           
            
            if selected_interval == "1m":
                max_date_diff = timedelta(days=7)
            elif selected_interval in ["5m", "15m", "30m", "90m"]: 
                max_date_diff = timedelta(days=60)
            elif selected_interval in ["60m", "1h"]:
                max_date_diff = timedelta(days=730)
            else:
                max_date_diff = None
            if selected_interval == "5d":
                min_diff = timedelta(days=5)
            elif selected_interval == "1wk":
                min_diff = timedelta(days=7)
            elif selected_interval == "1mo":
                min_diff = timedelta(days=30)
            elif selected_interval == "3mo":
                min_diff = timedelta(days=90)
            else:
                min_diff = None
                    
            if max_date_diff and (end - start) > max_date_diff and selected_interval !="1m" :
                st.error(f"The selected time interval '{selected_interval}' allows a maximum date range of {max_date_diff.days} days.")
            elif min_diff and (end-start) < min_diff and selected_interval !="1m":
                st.error(f"The selected time interval '{selected_interval}' requires a minimum date range of {min_diff.days} days.")
            elif selected_interval == "1m" :
                if (end-start) > timedelta(days=7):
                    st.error(f"The selected time interval '{selected_interval}' allows a maximum date range of {timedelta(days=7).days} days.")
                else:
                    Data = T.history(start=start, end=end, interval=selected_interval)
                    try:
                        Data.index = Data.index.tz_localize(None)
                    except KeyError:
                        pass
                            
                    st.dataframe(Data)
                            
                    Data = Data.reset_index()
                    fig0 = go.Figure()
                    if 'Datetime' in Data.columns: 
                        fig0.add_trace(go.Scatter(x=Data['Datetime'], y=Data['Close'], mode='lines', name='Close'))
                    else:
                        fig0.add_trace(go.Scatter(x=Data['Date'], y=Data['Close'], mode='lines', name='Close'))
                    fig0.update_layout(title='Stock Prices',xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig0)
            else:
                Data = T.history(start=start, end=end, interval=selected_interval)
                    
                try:
                    Data.index = Data.index.tz_localize(None)
                except KeyError:
                    pass
                
                        
                st.dataframe(Data)
                        
                Data = Data.reset_index()
                fig0 = go.Figure()
                if 'Datetime' in Data.columns: 
                    fig0.add_trace(go.Scatter(x=Data['Datetime'], y=Data['Close'], mode='lines', name='Close'))
                else:
                    fig0.add_trace(go.Scatter(x=Data['Date'], y=Data['Close'], mode='lines', name='Close'))
                fig0.update_layout(title='Stock Prices',xaxis_rangeslider_visible=True)
                st.plotly_chart(fig0)

            
        if selected == "TECHNICAL INDICATORS":
            
            st.header("Technical Indicators")
            data['SMA_50'] = data['Adj Close'].rolling(window=50).mean().round(2)
            data['SMA_200'] = data['Adj Close'].rolling(window=200).mean().round(2)
            
            def calculate_mfi(data, window=14):
                data['tp'] = (data['High'] + data['Low'] + data['Close']) / 3
                data['mf'] = data['tp'] * data['Volume']
                data['pmf'] = 0.0
                data['nmf'] = 0.0
                data.loc[data['tp'] > data['tp'].shift(1), 'pmf'] = data['mf']
                data.loc[data['tp'] < data['tp'].shift(1), 'nmf'] = data['mf']
                data['mfr'] = data['pmf'].rolling(window=window).sum() / data['nmf'].rolling(window=window).sum()
                data['mfi'] = 100 - (100 / (1 + data['mfr']))
                return data
            data_mfi = calculate_mfi(data)
            mfi_value = data_mfi['mfi'].iloc[-1]
            mfi_value = round(data_mfi['mfi'].iloc[-1], 2)
        
            data_reset = data.reset_index()
        
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], name="Prices"))
            fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name="SMA 50"))
            fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_200'], name="SMA 200"))
            fig1.update_layout(title="Stock Price with SMAs", xaxis_rangeslider_visible=True)
            
            fig_mfi = go.Figure()
            fig_mfi.add_trace(go.Scatter(x=data_mfi.index, y=data_mfi['mfi'], name="MFI"))
            fig_mfi.update_layout(title='Money Flow Index (MFI)',xaxis_title='Date',yaxis_title='MFI',xaxis_rangeslider_visible=True)
            
            col1,col2=st.columns(2)
            with col1:
                button1=st.button("Simple Moving Average")
            with col2:
                button2=st.button("Money Flow Index")
            if button1:
                st.plotly_chart(fig1)
                st.write("SMA-50 shows Short Term Average\n\n SMA-200 shows Long Term Average\n\n If in the graph:-\n\n  SMA-50 is above SMA-200 : Bullish Trend\n\n Price above of both SMA-50 and SMA-200 : Bullish Trend\n\n SMA-50 below SMA-200 : Bearish Trend\n\n Prices below of both SMA-50 and SMA-200 : Bearish Trend")
                st.button("Exit   ")
                
            if button2:
                st.metric(label="MFI", value=mfi_value) 
                st.plotly_chart(fig_mfi)
                st.write("MFI Index Value ranges from 0 - 100.\n\n MFI >= 80 means the stock is overbought and might face a downward correction.\n\n MFi <= 20 means the stock is oversold and might face a upward correction\n\n MFI between 20 and 80 means the stock is balanced.")
                st.button("Exit     ")
            
        if selected == "INFORMATION":
            st.header("Information")
            
            business_summary = T.info.get('longBusinessSummary')
            if business_summary:
                st.subheader("Business Summary")
                st.caption(business_summary)
                st.write("---")
            
            industry = T.info.get('industry')
            if industry:
                st.write(f"**Industry:** {industry}")
            
            sector = T.info.get('sector')
            if sector:
                st.write(f"Sector: {sector}")
                
            cap = T.info.get('marketCap')
            if industry:
                st.write(f"**Market Capitalisation**: $ {cap}")
                
            div = T.info.get('dividendRate')
            if industry:
                st.write(f"**Dividend Rate:** {div:.2f}")
            
            pe = T.info.get('trailingPE')
            if industry:
                st.write(f"**P/E Ratio:** {pe:.2f}")
            
            total_cash = T.info.get('totalCash')
            if total_cash:
                st.write(f"**Total Cash**: $ {total_cash}")
            
            total_debt = T.info.get('totalDebt')
            if total_debt:
                st.write(f"**Debt Amount**: $ {total_debt}")
            
            total_revenue = T.info.get('totalRevenue')
            if total_revenue:
                st.write(f"Total Revenue**: $ {total_revenue}")
            
            free_cash_flow = T.info.get('freeCashflow')
            if free_cash_flow:
                st.write(f"Free Cash Flow**: $ {free_cash_flow}")

            
            st.write("---")
            st.subheader("News")
            news = T.news
            if news:
                for item in news:
                    title = item['title']
                    source = item['publisher']
                    url = item['link']
                    
                    st.markdown(f"Title: {title} -- <a href='{url}' style='color: lightgrey;'>See More</a>", unsafe_allow_html=True)
                    st.caption(f"**Source:** {source}")
                   
          
        if selected == "FORECAST":
            st.header("Forecasting")
            st.write("---")
            n_years = st.slider("Months Of Prediction: ", 1, 24)
            period = n_years * 30
            
            # Preprocess the data
            df = data.reset_index()[["Date", "Close"]].copy()
            df["Date"] = pd.to_datetime(df["Date"])
            df["DayOfWeek"] = df["Date"].dt.dayofweek
            df = df[(df["DayOfWeek"] != 5) & (df["DayOfWeek"] != 6)]
            df = df.rename(columns={"Date": "ds", "Close": "y"})
            
            # Train the Prophet model
            m = Prophet(daily_seasonality=True, yearly_seasonality=True)
            m.fit(df)
            
            # Make future dataframe and predictions
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)
            forecast1 = forecast.rename(columns={'ds':'Date','yhat':'Predicted Prices','yhat_lower':'Predicted Lowest','yhat_upper':'Predicted Highest'})
            forelist = ['Date', 'Predicted Prices', 'Predicted Lowest', 'Predicted Highest']
            
            st.write("---")
            st.subheader("Forecast Data")
            st.write(forecast1[forelist])
            st.write('---')
            
            # Prediction interval
            st.subheader("Prediction in Interval of Time")
            Start = st.date_input('Enter start date', value=None)
            End = st.date_input('Enter end date', value=None)
            if Start != End:
                selected_forecast = forecast1.loc[(forecast1['Date'] > pd.to_datetime(Start)) & (forecast1['Date'] <= pd.to_datetime(End))]
                st.write(selected_forecast[forelist])
            st.write("---")
            
            # Forecasted Data Graphs
            st.subheader('Forecasted Data Graphs')
            st.write("Actual Prices v/s Predicted Prices")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicted Prices', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], mode='lines', name='Actual Prices', marker=dict(color='blue')))
            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)
            
            st.write("Forecast Components")
            fig2 = m.plot_components(forecast)
            st.write(fig2)
            
            st.button("Exit")
            st.write("---")
        
if selected=="HELP":
    st.write("---")
    st.header("Help")
    st.write("This Web application allow users to visualize and analyze the stock prices of different companies and predict their future performance based on various factors.\nUser can see various graphs and future predicted prices.\n\nThis a useful tool for investors and traders to make informed decisions about their investments and gain insights into the stock market trends.")
    st.write("Here you can see how to use stock analysis and prediction.\nSearch for a comapny and you can see it's current stats.\nMenu on the left can be used for various features. User can select to see GRAPHS, DATA, INFORMATION, TECHNICAL INDICATORS & FORECAST.\nUser can use given buttons options to get more information.")
    st.caption("Contact us :-\n\nIn case of any inconvienience or any issue, Report at Email : - stocks_analysis@gmail.com")
        
