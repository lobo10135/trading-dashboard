# app.py
import streamlit as st
from strategies import lunch, gap, rsl, hit  # 1. Hinzufügen des Imports

st.set_page_config(page_title="Trading Dashboard", page_icon="📈")
st.title("📈 Trading Dashboard")

# 2. Menüpunkt hinzufügen
option = st.sidebar.selectbox("Strategie", [
    "GBP Lunch Time", 
    "Gap and Go weekly", 
    "RSL Analyse S&P 500", 
    "Hit and Run"
])

# 3. Logik erweitern
if option == "GBP Lunch Time":
    lunch.run()
elif option == "Gap and Go weekly":
    gap.run()
elif option == "RSL Analyse S&P 500":
    rsl.run()
elif option == "Hit and Run":
    hit.run()
