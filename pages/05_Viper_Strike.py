import streamlit as st
import yfinance as yf
import pandas as pd
import os

# Seiten-Konfiguration
st.set_page_config(page_title="Viper Strike", layout="wide")

# Zentrierung der gesamten Seite
_, col_center, _ = st.columns([1, 2, 1])

with col_center:
    # 1. Großes Logo
    if os.path.exists("bulle.jpg"):
        st.image("bulle.jpg", use_container_width=True)

    # 2. Überschrift
    st.markdown("### 🐍 Viper Strike")

    def get_weekly_data():
        ticker = "ES=F"
        data = yf.Ticker(ticker).history(period="2mo", interval="1wk")
        
        if len(data) < 2:
            return None

        def format_de(val):
            return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        w1_data = data.iloc[-1]
        w2_data = data.iloc[-2]
        
        kw1 = w1_data.name.strftime("%V")
        kw2 = w2_data.name.strftime("%V")
        
        rb_w1 = abs(w1_data['Close'] - w1_data['Open'])
        rb_w2 = abs(w2_data['Close'] - w2_data['Open'])
        
        percent_change = ((rb_w1 - rb_w2) / rb_w2 * 100) if rb_w2 != 0 else 0.0
        tendenz = "Bullisch" if (w1_data['Close'] - w1_data['Open']) >= 0 else "Bearish"
        
        return {
            "Markt": "S&P 500 E-Mini",
            "Eröffnung (Mo)": format_de(w1_data['Open']),
            "Schluss (Fr)": format_de(w1_data['Close']),
            f"Real Body KW{kw2}": format_de(rb_w2),
            f"Real Body KW{kw1}": format_de(rb_w1),
            "Real Body %": percent_change, 
            "Tendenz": tendenz
        }

    if st.button("Analyse starten"):
        result = get_weekly_data()
        if result:
            df = pd.DataFrame([result])
            
            # Kopie für die Anzeige
            df_display = df.copy()
            df_display['Real Body %'] = df_display['Real Body %'].apply(lambda x: f"{x:+.2f}%".replace(".", ","))
            
            # Styler definieren
            def style_df(data):
                # Wir greifen auf die numerische Prozentänderung zu (aus result['Real Body %'])
                is_condition_met = abs(result['Real Body %']) < 20
                
                # Farben für Tendenz (nur wenn Bedingung erfüllt)
                def color_tendenz(val):
                    if is_condition_met:
                        color = 'green' if val == 'Bullisch' else 'red'
                        return f'color: {color}; font-weight: bold'
                    return 'color: black' # Standardfarbe wenn Bedingung nicht erfüllt
                
                # Farben für Real Body % (nur Schrift grün, wenn < 20%)
                def color_percent(val):
                    if is_condition_met:
                        return 'color: green; font-weight: bold'
                    return ''

                styler = data.style.map(color_tendenz, subset=['Tendenz'])
                styler = styler.map(color_percent, subset=['Real Body %'])
                return styler

            st.dataframe(style_df(df_display), use_container_width=True, hide_index=True)
        else:
            st.error("Daten konnten nicht geladen werden.")
