import streamlit as st

# Konfiguration
st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="centered")

# CSS für den Sidebar-Look (Rot beim Hovern, saubere Trennung)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #F0F2F6; }
    .sidebar-link {
        display: block;
        padding: 10px;
        color: #31333F;
        text-decoration: none;
        border-bottom: 1px solid #E6E9EF;
        font-weight: 500;
        transition: color 0.2s;
    }
    .sidebar-link:hover { color: #FF4B4B; }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR (Wie dein altes Menü)
with st.sidebar:
    st.title("Navigation")
    st.markdown('<a href="https://lunchtime.streamlit.app" class="sidebar-link">GBP Lunch Time</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://gapandgo.streamlit.app">02 Gap and Go</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://dein-rsl-url.streamlit.app" class="sidebar-link">03 RSL Analyse</a>', unsafe_allow_html=True)
    st.markdown('<a href="#" class="sidebar-link">04 Hit and Run</a>', unsafe_allow_html=True)
    st.markdown('<a href="#" class="sidebar-link">05 Viper Strike</a>', unsafe_allow_html=True)

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
