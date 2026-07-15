import streamlit as st

# Konfiguration
st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="centered")

# SIDEBAR - Ohne CSS-Injection, Nutzung von nativem Markdown
with st.sidebar:
    st.title("Strategie auswählen")
    
    # Markdown-Links sind nativ linksbündig, haben die Standardschriftgröße 
    # und keinen Button-Kasten drumherum.
    st.markdown("[01 GBP Lunch Time](https://lunchtime.streamlit.app)")
    st.markdown("[02 Gap and Go](https://gapandgo.streamlit.app)")
    st.markdown("[03 RSL Analyse](https://dein-rsl-url.streamlit.app)")
    st.markdown("[04 Hit and Run](#)")
    st.markdown("[05 Viper Strike](#)")

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
