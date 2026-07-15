import streamlit as st

# Konfiguration
st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="centered")

# SIDEBAR - Komplett ohne CSS-Injection, nur native Streamlit-Elemente
with st.sidebar:
    st.title("Strategie auswählen")
    
    # Nutzung von st.link_button für den nativen Look
    if st.link_button("01 GBP Lunch Time", "https://lunchtime.streamlit.app", use_container_width=True):
        pass
    if st.link_button("02 Gap and Go", "https://gapandgo.streamlit.app", use_container_width=True):
        pass
    if st.link_button("03 RSL Analyse", "https://dein-rsl-url.streamlit.app", use_container_width=True):
        pass
    if st.link_button("04 Hit and Run", "#", use_container_width=True):
        pass
    if st.link_button("05 Viper Strike", "#", use_container_width=True):
        pass

# HAUPTINHALT
st.image("bulle.jpg", use_container_width=True)

st.markdown("### Willkommen im Trading Dashboard")
st.write("Wähle links eine Strategie aus, um fortzufahren.")

st.markdown("""
<ul style="list-style-type: disc; color: #FFD700;">
    <li><b>01 GBP Lunch Time</b></li>
    <li><b>02 Gap and Go</b></li>
    <li><b>03 RSL Analyse</b></li>
    <li><b>04 Hit and Run</b></li>
    <li><b>05 Viper Strike</b></li>
</ul>
""", unsafe_allow_html=True)
