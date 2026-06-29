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

st.title("Trading Dashboard")

if not pages_exists:
    st.error("FEHLER: Der Ordner 'pages' wurde nicht gefunden. Bitte stelle sicher, dass er im gleichen Verzeichnis wie app.py liegt.")
else:
    st.success("System bereit: Der Ordner 'pages' wurde erkannt.")

st.markdown("""
### Willkommen!
Wähle in der linken Seitenleiste eine Strategie aus, um die Analyse zu starten.

* **01 GBP Lunch Time**
* **02 Gap and Go**
* **03 RSL Analyse**
* **04 Hit and Run**

---
*Hinweis: Wenn das Menü links nicht erscheint, lade die Seite im Browser neu (F5).*
""")
