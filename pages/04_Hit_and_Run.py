import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from lxml import html
import requests

st.set_page_config(page_title="Hit and Run", layout="wide")
st.title("🚀 Hit and Run Scanner")

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        tree = html.fromstring(requests.get(url, headers=headers).content)
        return [row.xpath('.//td')[0].text_content().strip().replace('.', '-') 
                for row in tree.xpath('//table[contains(@class, "wikitable")]//tr')[1:]]
    except: return []

if st.button("Scan starten"):
    tickers = get_sp500_tickers()
    results = []
    bar = st.progress(0)
    
    with st.spinner("Analysiere..."):
        for i, t in enumerate(tickers[:30]): # Begrenzt auf 30 für Schnelligkeit
            try:
                df = yf.Ticker(t).history(period="3mo")
                if len(df) >= 60:
                    adx = float(ta.adx(high=df['High'], low=df['Low'], close=df['Close'], length=14)['ADX_14'].iloc[-1])
                    if adx > 30:
                        results.append({"Ticker": t, "ADX": round(adx, 2), "Price": round(df['Close'].iloc[-1], 2)})
            except: continue
            bar.progress((i + 1) / 30)
            
    if results:
        st.dataframe(pd.DataFrame(results), use_container_width=True)
    else:
        st.warning("Keine Treffer gefunden.")
