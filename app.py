import streamlit as st

st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="centered")

# SIDEBAR: Nur noch diese eine Navigation existiert
with st.sidebar:
    st.title("Strategie auswählen")
    
    # Links im nativen Stil: keine Unterstreichung, keine Button-Kästen
    st.markdown("""
        <div style="margin-bottom: 15px;">
            <a href="https://lunchtime.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">GBP Lunch Time</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://gapandgo.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">Gap and Go</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://rslstrategie.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">RSL Analyse</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://hitandrun.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">Hit and Run</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://viperstrike.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">Viper Strike</a>
        </div>
    """, unsafe_allow_html=True)

# HAUPTINHALT
st.image("bulle.jpg", use_container_width=True)

st.markdown("### Willkommen im Trading Dashboard")
st.write("Wähle links eine Strategie aus, um fortzufahren.")

st.markdown("""
<ul style="list-style-type: disc; color: #FFD700;">
    <li><b>GBP Lunch Time</b></li>
    <li><b>Gap and Go</b></li>
    <li><b>RSL Analyse</b></li>
    <li><b>Hit and Run</b></li>
    <li><b>Viper Strike</b></li>
</ul>
""", unsafe_allow_html=True)
