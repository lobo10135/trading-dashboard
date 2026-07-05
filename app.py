import streamlit as st
import os

st.set_page_config(
    page_title="Trading Dashboard", 
    page_icon="📈",
    layout="centered"
)

# Prüfen, ob der pages-Ordner existiert (nur zur Diagnose)
pages_exists = os.path.exists("pages")

st.image("bulle.jpg", use_container_width=True)

if not pages_exists:
    st.error("FEHLER: Der Ordner 'pages' wurde nicht gefunden. Bitte stelle sicher, dass er im gleichen Verzeichnis wie app.py liegt.")

st.markdown("""
### Willkommen!
Wähle in der linken Seitenleiste eine Strategie aus, um die Analyse zu starten.

<ul style="list-style-type: disc; color: #FFD700;">
    <li><b>01 GBP Lunch Time (Einstieg 13 Uhr, bei TP die Position um 75% reduzieren und Stop= Einstand.)</b></li>
    <li><b>02 Gap and Go (Einstieg am Montag zur Handelseröffnung)</b></li>
    <li><b>03 RSL Analyse</b></li>
    <li><b>04 Hit and Run</b></li>
    <li><b>05 Viper Strike</b></li>
</ul>

---
""", unsafe_allow_html=True)
