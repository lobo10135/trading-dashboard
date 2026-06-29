import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz

st.set_page_config(page_title="GBP Lunch Time", layout="wide")

# Übersetzungstabelle für Wochentage
WOCENTAGE_DE = {
    "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag", "Sunday": "Sonntag"
}

_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    # Angepasster Titel mit essbarem Logo
    st.title("🍔 GBP Lunch Time")

    def check_gbp_lunch_momentum(ticker="GBPUSD=X"):
        london_tz = pytz.timezone("Europe/London")
        london_time = datetime.now(london_tz)
        
        is_weekday = london_time.weekday() in [0, 1, 2] 
        
        if not is_weekday:
            wochentag_de = WOCENTAGE_DE.get(london_time.strftime('%A'), london_time.strftime('%A'))
            st.warning(f"Heute ist {wochentag_de}. Die Strategie ist nur Mo-Mi aktiv.")
            return

        data = yf.Ticker(ticker).history(period="10d")
        
        if len(data) < 3:
            st.error("Nicht genügend Daten für die Berechnung.")
            return

        # Wochentage ermitteln und übersetzen
        day_yesterday = WOCENTAGE_DE.get(data.index[-2].strftime('%A'), data.index[-2].strftime('%A'))
        day_before = WOCENTAGE_DE.get(data.index[-3].strftime('%A'), data.index[-3].strftime('%A'))
        
        close_yesterday = data['Close'].iloc[-2]
        close_day_before = data['Close'].iloc[-3]
        current_price = data['Close'].iloc[-1]
        
        momentum_percent = (close_yesterday / close_day_before) * 100
        
        st.write(f"**Aktuelle London Zeit:** {london_time.strftime('%H:%M:%S')}")
        st.write("---")
        st.subheader("Marktdaten-Analyse")
        st.write(f"Schlusskurs Vorgestern ({day_before}): **{close_day_before:.5f}**")
        st.write(f"Schlusskurs Gestern ({day_yesterday}): **{close_yesterday:.5f}**")
        st.metric("Momentum", f"{momentum_percent:.2f}%")
        
        if momentum_percent < 99.5: # 0.995 entspricht 99.5%
            st.success("✅ Bedingung erfüllt: Momentum ist um mehr als 0,5% gefallen.")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Aktueller Kurs", f"{current_price:.5f}")
            c2.metric("Stopkurs", f"{current_price - 0.0110:.5f}")
            c3.metric("Take Profit", f"{current_price + 0.0040:.5f}")
        else:
            st.error("❌ Bedingung nicht erfüllt: Momentum-Rückgang zu gering.")

    if st.button("Analyse starten"):
        check_gbp_lunch_momentum()
