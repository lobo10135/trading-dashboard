import streamlit as st

st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="centered")

with st.sidebar:
    st.title("Strategie auswählen")
    
    # Wir benutzen ein einfaches <div>, um den Text wie im Menü zu halten,
    # aber ohne die Browser-Standard-Link-Formatierung (Blau/Unterstrichen).
    # Das 'style' hier dient nur dazu, den Link wie normalen Text aussehen zu lassen.
    st.markdown("""
        <div style="margin-bottom: 10px;">
            <a href="https://lunchtime.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">01 GBP Lunch Time</a>
        </div>
        <div style="margin-bottom: 10px;">
            <a href="https://gapandgo.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">02 Gap and Go</a>
        </div>
        <div style="margin-bottom: 10px;">
            <a href="https://dein-rsl-url.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">03 RSL Analyse</a>
        </div>
        <div style="margin-bottom: 10px;">
            <a href="#" style="text-decoration: none; color: inherit; font-size: 14px;">04 Hit and Run</a>
        </div>
        <div style="margin-bottom: 10px;">
            <a href="#" style="text-decoration: none; color: inherit; font-size: 14px;">05 Viper Strike</a>
        </div>
    """, unsafe_allow_html=True)

# HAUPTINHALT
st.image("bulle.jpg", use_container_width=True)
st.markdown("### Willkommen im Trading Dashboard")
st.write("Wähle links eine Strategie aus, um fortzufahren.")
