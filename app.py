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
        <div style="margin-bottom: 15px;">
            <a href="https://watchlistperfect.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">Watchlist</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://swing07.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">Swing weekly</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://breakout08.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">Breakout weekly</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://180strategy.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">180</a>
        </div>
        <div style="margin-bottom: 15px;">
            <a href="https://180weekly.streamlit.app" style="text-decoration: none; color: inherit; font-size: 14px;">180`s weekly</a>
        </div>        
        
    """, unsafe_allow_html=True)

# HAUPTINHALT
st.image("bulle.jpg", use_container_width=True)

st.markdown("### Willkommen im Trading Dashboard")
st.write("Wähle links eine Strategie aus, um fortzufahren.")

st.markdown("""
<ul style="list-style-type: disc; color: #FFD700;">
    <li><b>GBP Lunch Time (Einstieg 13 Uhr, bei TP die Position um 75% reduzieren und Stop= Einstand.)</b></li>
    <li><b>Gap and Go (Einstieg am Montag zur Handelseröffnung)</b></li>
    <li><b>RSL Analyse</b></li>
    <li><b>Hit and Run</b></li>
    <li><b>Viper Strike</b></li>
    <li><b>Watchlist</b></li>
    <li><b>Swing weekly</b></li>
    <li><b>Breakout weekly</b></li>
    <li><b>180</b></li>
    <li><b>180`s weekly</b></li>    
</ul>
""", unsafe_allow_html=True)
