import streamlit as st

# Konfiguration der Hauptseite
st.set_page_config(
    page_title="Trading Dashboard", 
    page_icon="📈",
    layout="centered"
)

# Dein Bild oben zentriert anzeigen
st.image("bulle.jpg", use_container_width=True)

# Überschrift und Begrüßung
st.title("Trading Dashboard")
st.markdown("""
### Willkommen!
Wähle in der linken Seitenleiste eine Strategie aus, um die Analyse zu starten:

* **01 GBP Lunch Time**: Momentum-Analyse für das Währungspaar GBP/USD.
* **02 Gap and Go**: Wochenend-Gap-Analyse für Indizes.
* **03 RSL Analyse**: Relative Stärke nach Levy für S&P 500 Werte.
* **04 Hit and Run**: ADX-basierter Scanner für Trendaktien.

---
*Die Aufteilung in separate Seiten sorgt für maximale Stabilität und Performance deiner App.*
""")

# Optional: Ein kleiner Hinweis, falls jemand die App aufruft
st.info("💡 Tipp: Navigiere einfach über das Menü links zu deiner gewünschten Strategie.")
