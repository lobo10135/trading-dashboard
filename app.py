import streamlit as st
from strategies import lunch, gap, rsl, hit

st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { text-align: center; }
    h1, h2, h3 { text-align: center; }
    div.stButton > button { margin: 0 auto; display: block; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Trading Dashboard")

option = st.sidebar.selectbox("Strategie", [
    "GBP Lunch Time", 
    "Gap and Go weekly", 
    "RSL Analyse S&P 500", 
    "Hit and Run"
])

if option == "GBP Lunch Time":
    lunch.run()
elif option == "Gap and Go weekly":
    gap.run()
elif option == "RSL Analyse S&P 500":
    rsl.run()
elif option == "Hit and Run":
    hit.run()
