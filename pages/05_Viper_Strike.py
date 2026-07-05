import streamlit as st
import yfinance as yf
import pandas as pd
import os
from datetime import timedelta

# Seiten-Konfiguration
st.set_page_config(page_title="Viper Strike", layout="wide")

# Zentrierung der Seite
_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    # 1. Logo
    if os.path.exists("bulle.jpg"):
        st.image("bulle.jpg", use_container_width=True)

    # 2. Überschrift
    st.markdown("### 🐍 Viper Strike")

    def get_market_data(ticker, name, rb_threshold_pct, stop_offset_pct, stop_diff, tp_offset, hold_weeks):
        # 3 Wochen laden
        data = yf.Ticker(ticker).history(period="3mo", interval="1wk")
        if len(data) < 3:
            return None

        def format_de(val):
            return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # w0: Aktuell, w1: Vorwoche
        w0_data = data.iloc[-1]
        w1_data = data.iloc[-2]
        
        # Berechnungen
        rb_w0 = abs(w0_data['Close'] - w0_data['Open'])
        range_w1 = abs(w1_data['High'] - w1_data['Low'])
        
        # Real Body %: (Real Body aktuell / Range Vorwoche) * 100
        percent_change = ((rb_w0 / range_w1) * 100) if range_w1 != 0 else 0.0
        
        # Bedingung prüfen (Threshold)
        is_condition_met = abs(percent_change) < rb_threshold_pct
        is_bullish = (w0_data['Close'] - w0_data['Open']) >= 0
        tendenz = "Bullisch" if is_bullish else "Bearish"
        
        # Stop Buy/Sell: Basierend auf Schlusskurs (W0) und Range der Vorwoche (W1)
        stop_value = (w0_data['Close'] + (range_w1 * stop_offset_pct)) if is_bullish else (w0_data['Close'] - (range_w1 * stop_offset_pct))
        
        # Stop und TP Berechnungen
        stop_calculated = stop_value - stop_diff if is_condition_met else 0.0
        tp_calculated = (stop_value + tp_offset) if (tp_offset is not None and is_condition_met) else None
        
        # Haltedauer
        halte_datum = w0_data.name + timedelta(weeks=hold_weeks) + timedelta(days=4)
        
        return {
            "Markt": name,
            "Eröffnung (Mo)": format_de(w0_data['Open']),
            "Schluss (Fr)": format_de(w0_data['Close']),
            "Real Body aktuell": format_de(rb_w0),
            "Range Vorwoche": format_de(range_w1),
            "Real Body %": percent_change,
            "Tendenz": tendenz,
            "Stop Buy/Sell": format_de(stop_value) if is_condition_met else "-",
            "Stop": format_de(stop_calculated) if is_condition_met else "-",
            "TP": format_de(tp_calculated) if tp_calculated is not None else "-",
            "Haltedauer": halte_datum.strftime("%d.%m.%Y")
        }

    if st.button("Analyse starten"):
        results = [
            # S&P 500: 20% Schwellenwert, 20% Offset, -420 Stop, +420 TP, 4 Wochen
            get_market_data("ES=F", "S&P 500 E-Mini", 20, 0.20, 420, 420, 4),
            # FDAX: 60% Schwellenwert, 50% Offset, -2000 Stop, Kein TP, 5 Wochen
            get_market_data("^GDAXI", "FDAX", 60, 0.50, 2000, None, 5)
        ]
        
        results = [r for r in results if r]
        
        if results:
            df = pd.DataFrame(results)
            # Formatierung für die Anzeige
            df_display = df.copy()
            df_display['Real Body %'] = df_display['Real Body %'].apply(lambda x: f"{x:.2f}%".replace(".", ","))
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.error("Daten konnten nicht geladen werden.")
