import streamlit as st
# Importiere die Module
from strategies import lunch, gap, rsl, hit 

st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="wide")

# ... CSS ...

option = st.sidebar.selectbox("Strategie", [
    "GBP Lunch Time", 
    "Gap and Go weekly", 
    "RSL Analyse S&P 500", 
    "Hit and Run"
])

# Hier rufst du jetzt die FUNKTIONSNAMEN auf, die du in den Dateien hast
if option == "GBP Lunch Time":
    lunch.check_gbp_lunch_momentum() # <-- Hier den alten Namen einfügen!

elif option == "Gap and Go weekly":
    # Hier müsstest du schauen, wie die Funktion in gap.py heißt
    gap.check_weekend_gap(...) 

elif option == "RSL Analyse S&P 500":
    rsl.calculate_rsl_26_weeks() # <-- Hier den alten Namen einfügen!

elif option == "Hit and Run":
    hit.run() # Das war die einzige neue, die wir so definiert hatten
