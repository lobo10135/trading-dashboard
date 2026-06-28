import streamlit as st
import yfinance as yf
import datetime

st.set_page_config(page_title="Gap and Go", layout="wide")
st.title("📈 Gap and Go Weekly")

def check_weekend_gap(symbol, name, min_g, g_type, stop, tp):
    # Daten für den letzten Monat laden
    hist = yf.Ticker(symbol).history(period="1mo")
    if len(hist) < 2: 
        st.error(f"Keine Daten für {name}")
        return
    
    vor, neu = hist.iloc[-2], hist.iloc[-1]
    open_p = float(neu["Open"])
    
    if g_type == "up":
        gap = ((open_p - float(vor["High"])) / float(vor["High"])) * 100
        if gap > min_g:
            st.success(f"🟢 {name} UP-GAP: {gap:.2f}% | Stop: {open_p-stop:.2f} | TP: {open_p+tp:.2f}")
    else:
        gap = abs((float(vor["Low"]) - open_p) / float(vor["Low"])) * 100
        if gap > min_g:
            st.error(f"🔴 {name} DOWN-GAP: {gap:.2f}% | Stop: {open_p+stop:.2f} | TP: {open_p-tp:.2f}")

if st.button("Alle Märkte scannen"):
    with st.spinner("Scanne Märkte..."):
        check_weekend_gap("^GDAXI", "DAX 40", 0.0, "up", 1800, 0)
        check_weekend_gap("ES=F", "S&P 500", 0.0, "up", 300, 600)
        # Hier kannst du beliebig weitere Symbole hinzufügen
        st.info("Scan abgeschlossen.")
