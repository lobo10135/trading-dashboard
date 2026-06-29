import streamlit as st
import yfinance as yf
from datetime import datetime

# Seiten-Konfiguration
st.set_page_config(page_title="GBP Lunch Time", layout="wide")

# Zentrierung der gesamten Seite durch Spalten
_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    st.title("GBP Lunch Time Strategie")

    def check_gbp_lunch_momentum(ticker="GBPUSD=X"):
        # Wochentag prüfen
        today = datetime.now().weekday()
        
        output = []
        output.append("=================================================================")
        output.append("      GBP Lunch Time        ")
        output.append("=================================================================")
        
        if today not in [0, 1, 2]:
            output.append(f"Heute ist {datetime.now().strftime('%A')}. Die Strategie ist heute inaktiv (Mo-Mi).")
            st.text("\n".join(output))
            return False

        # Daten laden
        data = yf.Ticker(ticker).history(period="10d")
        
        if len(data) < 3:
            output.append("Nicht genügend Daten für die Momentum-Berechnung verfügbar.")
            st.text("\n".join(output))
            return False

        # Berechnung
        close_yesterday = data['Close'].iloc[-1]
        close_day_before = data['Close'].iloc[-2]
        current_price = yf.Ticker(ticker).info.get('regularMarketPrice') or data['Close'].iloc[-1]
        
        day_yesterday = data.index[-1].strftime('%A')
        day_before = data.index[-2].strftime('%A')
        
        momentum = (close_yesterday / close_day_before)
        momentum_percent = momentum * 100
        
        output.append(f"Schlusskurs Vorgestern ({day_before}): {close_day_before:.5f}")
        output.append(f"Schlusskurs Gestern    ({day_yesterday}): {close_yesterday:.5f}")
        output.append(f"Momentum:               {momentum_percent:.2f}%")
        
        if momentum < 0.995:
            output.append("✅ Bedingung erfüllt: Momentum ist um mehr als 0,5% gefallen.")
            stop_kurs = current_price - 0.0110
            take_profit = current_price + 0.0040
            output.append(f"Aktueller Kurs:         {current_price:.5f}")
            output.append(f"Stopkurs:               {stop_kurs:.5f}")
            output.append(f"Take Profit 75%:        {take_profit:.5f}")
        else:
            output.append("❌ Bedingung nicht erfüllt: Momentum-Rückgang zu gering.")
        
        # Ausgabe innerhalb der zentrierten Spalte
        st.text("\n".join(output))

    # Button zentriert (durch Platzierung in der Mittelspalte)
    if st.button("Analyse starten"):
        check_gbp_lunch_momentum()
