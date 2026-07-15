import streamlit as st

st.set_page_config(
    page_title="Trading Dashboard", 
    page_icon="📈",
    layout="centered"
)

st.image("bulle.jpg", use_container_width=True)

st.markdown("### Willkommen!")
st.write("Wähle eine Strategie aus:")

# Hier erstellst du die Links zu deinen anderen Repositories
# Sobald du diese auf Streamlit Cloud veröffentlicht hast, 
# erhältst du von Streamlit eine URL (z.B. https://deinname-lunch.streamlit.app)

with st.sidebar:
    st.title("Strategien")
    st.markdown("[01 GBP Lunch Time](https://lunchtime.app)")
    st.markdown("[02 Gap and Go](https://gapandgo.app)")
    st.markdown("[03 RSL Analyse](https://deinname-rsl.streamlit.app)")

# Dein HTML-Block bleibt erhalten
st.markdown("""
<ul style="list-style-type: disc; color: #FFD700;">
    <li><b>01 GBP Lunch Time</b></li>
    <li><b>02 Gap and Go</b></li>
    <li><b>03 RSL Analyse</b></li>
    <li><b>04 Hit and Run</b></li>
    <li><b>05 Viper Strike</b></li>
</ul>
""", unsafe_allow_html=True)
