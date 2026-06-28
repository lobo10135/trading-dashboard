import streamlit as st
import yfinance as yf
import pandas as pd
import time
import requests
import datetime
from datetime import datetime as dt
import bs4 as bs
from lxml import html
from fpdf import FPDF

# --- Konfiguration ---
st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { text-align: center; }
    h1, h2, h3 { text-align: center; }
    div.stButton > button { margin: 0 auto; display: block; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Trading Dashboard")

# --- Strategie: Hit and Run (Scanner) ---
@st.cache_data(ttl=86400)
def get_sp500_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        tree = html.fromstring(response.content)
        table = tree.xpath('//table[contains(@class, "wikitable")]')[0]
        data = []
        for row in table.xpath('.//tr')[1:]:
            cells = row.xpath('.//td')
            data.append({"Ticker": cells[0].text_content().strip(), "Wert": cells[1].text_content().strip(), "Sektor": cells[3].text_content().strip()})
        return data
    except: return []

def analyze_ticker_hit_run(ticker, mode="long"):
    try:
        # Sicherer Import
        import pandas_ta as ta
        stock = yf.Ticker(ticker)
        df = stock.history(period="3mo", auto_adjust=True)
        if len(df) < 60: return None
        prices = df['Close'].dropna().astype(float).tolist()
        current_price = prices[-1]
        adx_series = ta.adx(high=df['High'], low=df['Low'], close=df['Close'], length=14)
        current_adx = float(adx_series['ADX_14'].iloc[-1])
        if pd.isna(current_adx) or current_adx <= 30 or current_price <= 30: return None
        
        if mode == "long":
            cond1 = current_price > (sum(prices[-10:]) / 10)
            cond2 = current_price > (sum(prices[-50:]) / 50)
            cond3 = df.iloc[-10:]['High'].max() >= df.iloc[-52:-10]['High'].max()
            col_name = "2 month High"
        else:
            cond1 = current_price < (sum(prices[-10:]) / 10)
            cond2 = current_price < (sum(prices[-50:]) / 50)
            cond3 = df.iloc[-10:]['Low'].min() <= df.iloc[-52:-10]['Low'].min()
            col_name = "2 month Low"
        if not (cond1 and cond2 and cond3): return None
        return {"ADX": round(current_adx, 2), "Price": round(current_price, 2), "GD10": "🟢", "GD50": "🟢", col_name: "🟢"}
    except: return None

# --- Hier deine anderen Strategien einfügen ---
# (Füge hier deine Funktionen check_gbp_lunch_momentum, check_weekend_gap, calculate_rsl_26_weeks ein)
# ...

# --- UI Menü ---
option = st.sidebar.selectbox("Strategie", ["GBP Lunch Time", "Gap and Go weekly", "RSL Analyse S&P 500", "Hit and Run"])

if option == "Hit and Run":
    st.header("🚀 Hit and Run Scanner")
    if st.button("Scan starten"):
        sp_data = get_sp500_data()
        long_res, short_res = [], []
        bar = st.progress(0)
        for i, item in enumerate(sp_data):
            t_clean = item['Ticker'].replace('.', '-')
            res_l = analyze_ticker_hit_run(t_clean, mode="long")
            if res_l: long_res.append({**item, **res_l})
            res_s = analyze_ticker_hit_run(t_clean, mode="short")
            if res_s: short_res.append({**item, **res_s})
            bar.progress((i + 1) / len(sp_data))
        # Hier display_results aufrufen...
        st.success("Scan beendet")
# ... (restliche if-else Logik für die anderen Strategien)
