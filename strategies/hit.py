import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
import requests
from lxml import html

st.set_page_config(page_title="Hit and Run Scanner", layout="wide")

# CSS für die vollständige Zentrierung
st.markdown("""
    <style>
    .stApp { text-align: center; }
    h1, h2, h3 { text-align: center; }
    .stProgress { max-width: 500px; margin: 0 auto; }
    div.stButton > button { margin: 0 auto; display: block; }
    </style>
""", unsafe_allow_html=True)

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
            # Index 0: Ticker, Index 1: Name, Index 3: Sektor
            data.append({
                "Ticker": cells[0].text_content().strip(), 
                "Wert": cells[1].text_content().strip(),
                "Sektor": cells[3].text_content().strip()
            })
        return data
    except: return []

def analyze_ticker(ticker, mode="long"):
    try:
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

# Helper für die Spaltenkonfiguration und Anzeige
def display_results(results, title, icon):
    st.subheader(f"{icon} {title}")
    if results:
        df = pd.DataFrame(results).sort_values("ADX", ascending=False)
        # Sicherstellen der Reihenfolge: Ticker, Wert, Sektor, dann der Rest
        cols = ["Ticker", "Wert", "Sektor", "ADX", "Price", "GD10", "GD50"]
        # Die Spalte "2 month High" oder "2 month Low" dynamisch finden
        last_col = [c for c in df.columns if "2 month" in c][0]
        cols.append(last_col)
        df = df[cols]
        
        col_config = {
            "GD10": st.column_config.TextColumn("GD10", alignment="right"),
            "GD50": st.column_config.TextColumn("GD50", alignment="right"),
            last_col: st.column_config.TextColumn(last_col, alignment="right"),
        }
        st.dataframe(df, use_container_width=True, hide_index=True, column_config=col_config)
    else:
        st.warning("Keine Treffer gefunden.")

st.title("🚀 Hit and Run Scanner")
st.write("Zeigt nur Aktien mit ADX > 30, Preis > 30 und voll erfüllten Trend-Bedingungen.")

if st.button("Scan starten"):
    sp_data = get_sp500_data()
    long_results, short_results = [], []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, item in enumerate(sp_data):
        t_clean = item['Ticker'].replace('.', '-')
        res_long = analyze_ticker(t_clean, mode="long")
        if res_long: long_results.append({**item, **res_long})
        res_short = analyze_ticker(t_clean, mode="short")
        if res_short: short_results.append({**item, **res_short})
        progress_bar.progress((i + 1) / len(sp_data))
        status_text.text(f"Analysiere: {item['Ticker']}")
        time.sleep(0.05)
        
    status_text.empty(); progress_bar.empty()
    display_results(long_results, "Long-Treffer", "🟢")
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    display_results(short_results, "Short-Treffer", "🔴")
