import streamlit as st
import yfinance as yf
from datetime import datetime as dt

st.set_page_config(page_title="GBP Lunch Time", layout="wide")
st.title("🕒 GBP Lunch Time Momentum")

def check_gbp_lunch_momentum(ticker="GBPUSD=X"):
    today = dt.now().weekday()
    # Strategie ist nur Mo-Mi aktiv (0, 1, 2)
    if today not in [0, 1, 2]:
        st.warning(f"Heute ist {dt.now().strftime('%A')}. Strategie ist inaktiv (nur Mo-Mi).")
        return

    data = yf.Ticker(ticker).history(period="10d")
    if len(data) < 3:
        st.error("Nicht genügend Daten verfügbar.")
        return
        
    close_yesterday = data['Close'].iloc[-1]
    close_day_before = data['Close'].iloc[-2]
    current_price = data['Close'].iloc[-1] # Annahme für Echtzeitkurs
    
    momentum = (close_yesterday / close_day_before) * 100
    
    st.metric("Momentum zum Vortag", f"{momentum:.2f}%")
    
    if momentum < 99.5:
        st.success("✅ Bedingung erfüllt: Momentum ist um mehr als 0,5% gefallen.")
        st.metric("Stopkurs", f"{current_price - 0.0110:.5f}")
        st.metric("Take Profit 75%", f"{current_price + 0.0040:.5f}")
    else:
        st.error("❌ Bedingung nicht erfüllt: Rückgang zu gering.")

if st.button("Markt prüfen"):
    check_gbp_lunch_momentum()
