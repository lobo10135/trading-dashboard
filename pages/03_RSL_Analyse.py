import streamlit as st
import yfinance as yf
import pandas as pd
import bs4 as bs
import requests

st.set_page_config(page_title="RSL Analyse", layout="wide")
st.title("📊 RSL Analyse S&P 500")

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(resp.text, "lxml")
        table = soup.find("table", {"id": "constituents"})
        return [r.findAll("td")[0].text.strip().replace(".", "-") for r in table.findAll("tr")[1:]]
    except Exception as e:
        st.error(f"Fehler beim Laden der Ticker: {e}")
        return []

if st.button("Analyse starten"):
    with st.spinner("Berechne RSL-Werte..."):
        tickers = get_sp500_tickers()
        if tickers:
            # Laden der Daten
            raw = yf.download(tickers, period="1y", group_by='ticker', progress=False)
            res = []
            for t in tickers:
                if t in raw.columns.levels[0]:
                    df = raw[t].dropna()
                    if len(df) >= 130:
                        rsl = float(df['Close'].iloc[-1] / df['Close'].iloc[-130:].mean())
                        res.append({"Ticker": t, "RSL": round(rsl, 4)})
            
            df_final = pd.DataFrame(res).sort_values("RSL", ascending=False)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("TOP 125")
                st.dataframe(df_final.head(125), use_container_width=True)
            with col2:
                st.subheader("FLOP 125")
                st.dataframe(df_final.tail(125), use_container_width=True)
        else:
            st.warning("Keine Ticker gefunden.")
