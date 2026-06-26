import streamlit as st
import yfinance as yf
import datetime
from datetime import datetime as dt

# --- Konfiguration ---
st.set_page_config(page_title="Lobo10135 Trading Suite", page_icon="📈")

# CSS-Injection, um das Cursor-Verhalten global zu unterbinden
st.markdown("""
    <style>
    /* Erzwingt den Standard-Cursor für alle interaktiven Elemente */
    button, [data-baseweb="select"], [data-baseweb="select"] *, div[role="combobox"], input {
        cursor: default !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Trading Dashboard")

# --- Strategie 1: GBP Lunch Time ---
def check_gbp_lunch_momentum(ticker="GBPUSD=X"):
    today = dt.now().weekday()
    if today not in [0, 1, 2]:
        st.warning(f"Heute ist {dt.now().strftime('%A')}. Die Strategie ist heute inaktiv (Mo-Mi).")
        return False
    data = yf.Ticker(ticker).history(period="10d")
    if len(data) < 3:
        st.error("Nicht genügend Daten verfügbar.")
        return False
    close_yesterday = data['Close'].iloc[-1]
    close_day_before = data['Close'].iloc[-2]
    current_price = yf.Ticker(ticker).info.get('regularMarketPrice') or data['Close'].iloc[-1]
    momentum = (close_yesterday / close_day_before)
    momentum_percent = momentum * 100
    st.write(f"Schlusskurs Vorgestern: {close_day_before:.5f}")
    st.write(f"Schlusskurs Gestern: {close_yesterday:.5f}")
    st.metric("Momentum", f"{momentum_percent:.2f}%")
    if momentum < 0.995:
        st.success("✅ Bedingung erfüllt: Momentum ist um mehr als 0,5% gefallen.")
        stop_kurs = current_price - 0.0110
        take_profit = current_price + 0.0040
        st.write(f"Aktueller Kurs: {current_price:.5f}")
        st.metric("Stopkurs", f"{stop_kurs:.5f}")
        st.metric("Take Profit 75%", f"{take_profit:.5f}")
    else:
        st.error("❌ Bedingung nicht erfüllt: Momentum-Rückgang zu gering.")

# --- Strategie 2: Gap and Go weekly ---
def check_weekend_gap(hist, market_name, min_gap_percent=0.0, gap_type="up", stop_distance=None, take_profit_distance=None, holding_weeks=None):
    if hist is None or hist.empty or len(hist) < 2:
        st.text(f"Fehler: Keine ausreichenden Daten für {market_name} verfügbar.")
        return

    vorwoche_data, neuwoche_data = None, None
    for i in range(len(hist) - 1, 0, -1):
        if (hist.index[i].date() - hist.index[i - 1].date()).days >= 2:
            neuwoche_data, vorwoche_data = hist.iloc[i], hist.iloc[i - 1]
            break
    if vorwoche_data is None: neuwoche_data, vorwoche_data = hist.iloc[-1], hist.iloc[-2]

    neuwoche_open = float(neuwoche_data["Open"])
    
    def get_exit_friday(start_date, weeks):
        target_date = start_date.date() + datetime.timedelta(weeks=weeks)
        days_to_friday = 4 - target_date.weekday() if target_date.weekday() <= 4 else 4 - target_date.weekday() + 7
        return (target_date + datetime.timedelta(days=days_to_friday)).strftime("%d.%m.%Y")

    if gap_type == "up":
        vorwoche_high = float(vorwoche_data["High"])
        gap_punkte = neuwoche_open - vorwoche_high
        gap_prozent = (gap_punkte / vorwoche_high) * 100
        if gap_punkte > 0 and gap_prozent > min_gap_percent:
            st.success(f"🟢 {market_name.upper()} UP-GAP FOUND")
            st.write(f"Lücke: +{gap_punkte:.4f} (+{gap_prozent:.2f}%)")
            if stop_distance: st.write(f"Stop: {neuwoche_open - stop_distance:.4f}")
            if take_profit_distance: st.write(f"TP: {neuwoche_open + take_profit_distance:.4f}")
            if holding_weeks: st.write(f"Haltedauer: {holding_weeks} Wochen (Exit: {get_exit_friday(neuwoche_data.name, holding_weeks)})")
        else: st.info(f"ℹ️ {market_name}: Kein Up-Gap > {min_gap_percent}%")

    elif gap_type == "down":
        vorwoche_low = float(vorwoche_data["Low"])
        gap_punkte = vorwoche_low - neuwoche_open
        gap_prozent = abs((gap_punkte / vorwoche_low) * 100)
        if (neuwoche_open < vorwoche_low) and (gap_prozent > min_gap_percent):
            st.error(f"🔴 {market_name.upper()} DOWN-GAP FOUND")
            st.write(f"Lücke: -{gap_punkte:.4f} (-{gap_prozent:.2f}%)")
            if stop_distance: st.write(f"Stop: {neuwoche_open + stop_distance:.4f}")
            if take_profit_distance: st.write(f"TP: {neuwoche_open - take_profit_distance:.4f}")
            if holding_weeks: st.write(f"Haltedauer: {holding_weeks} Wochen (Exit: {get_exit_friday(neuwoche_data.name, holding_weeks)})")
        else: st.info(f"ℹ️ {market_name}: Kein Down-Gap > {min_gap_percent}%")

def fetch_data(ticker_symbol):
    try:
        hist = yf.Ticker(ticker_symbol).history(period="10d")
        return hist if not hist.empty else None
    except: return None

# --- UI Menü ---
option = st.sidebar.selectbox("Strategie", ["GBP Lunch Time", "Gap and Go weekly"])

if option == "GBP Lunch Time":
    st.header("GBP Lunch Time")
    if st.button("Markt prüfen"): check_gbp_lunch_momentum()

elif option == "Gap and Go weekly":
    st.header("Gap and Go weekly")
    if st.button("Alle Märkte prüfen"):
        m = dt.now().month
        n = dt.now().strftime("%B")
        
        check_weekend_gap(fetch_data("^GDAXI"), "DAX 40", 0.0, "up", 1800.0, None, 11)
        if m in [1, 8]: st.write(f"⏭️ EuroStoxx 50: Pause im {n}")
        else: check_weekend_gap(fetch_data("^STOXX50E"), "EuroStoxx 50", 0.0, "up", 240.0, None, 8)
        check_weekend_gap(fetch_data("ES=F"), "S&P 500 E-Mini Future", 0.0, "up", 300.0, 600.0, 10)
        check_weekend_gap(fetch_data("^NDX"), "Nasdaq 100", 5.0, "up", 1250.0, 1500.0, 15)
        rut = fetch_data("^RUT")
        check_weekend_gap(rut, "Russell 2000 (Up)", 0.0, "up", 340.0, 200.0, 10)
        if m in [7, 8]: st.write(f"⏭️ Russell 2000 (Down): Pause im {n}")
        else: check_weekend_gap(rut, "Russell 2000 (Down)", 10.0, "down", 200.0, 240.0, 0)
        dji = fetch_data("^DJI")
        if m in [1, 7]: st.write(f"⏭️ Dow Jones (Up): Pause im {n}")
        else: check_weekend_gap(dji, "Dow Jones (Up)", 0.0, "up", 5000.0, None, 10)
        if m in [7, 8]: st.write(f"⏭️ Dow Jones (Down): Pause im {n}")
        else: check_weekend_gap(dji, "Dow Jones (Down)", 0.0, "down", 3800.0, 3000.0, 0)
        if m in [2, 3]: st.write(f"⏭️ T-Bond (Up): Pause im {n}")
        else: check_weekend_gap(fetch_data("ZB=F"), "T-Bond (Up)", 0.0, "up", 11.0, 28.0, 11)
        if m in [2, 3]: st.write(f"⏭️ T-Note (Up): Pause im {n}")
        else: check_weekend_gap(fetch_data("ZN=F"), "T-Note (Up)", 0.0, "up", 8.0, None, 11)
        check_weekend_gap(fetch_data("EUN3.DE"), "Bund Future", 5.0, "up", 8.0, 16.0, 19)
        if m == 9: st.write(f"⏭️ WTI (Up): Pause im {n}")
        else: check_weekend_gap(fetch_data("CL=F"), "WTI Rohöl", 0.0, "up", 35.0, None, 16)
        rb = fetch_data("RB=F")
        check_weekend_gap(rb, "Gasoline (Up)", 15.0, "up", 83.33, 83.33, 20)
        if m == 3: st.write(f"⏭️ Gasoline (Down): Pause im {n}")
        else: check_weekend_gap(rb, "Gasoline (Down)", 5.0, "down", 38.10, 166.67, 13)
        if m in [4, 5, 6]: st.write(f"⏭️ Cotton (Up): Pause im {n}")
        else: check_weekend_gap(fetch_data("CT=F"), "Cotton", 7.0, "up", 17.0, 28.0, 7)
        if m == 7: st.write(f"⏭️ Sugar (Up): Pause im {n}")
        else: check_weekend_gap(fetch_data("SB=F"), "Sugar No.11", 5.0, "up", 358.0, None, 3)
        oj = fetch_data("OJ=F")
        if m in [4, 5, 6, 12]: st.write(f"⏭️ OJ (Up): Pause im {n}")
        else: check_weekend_gap(oj, "Orange Juice (Up)", 0.0, "up", 34.0, 187.0, 19)
        if m in [3, 4, 5, 6, 7, 8]: st.write(f"⏭️ OJ (Down): Pause im {n}")
        else: check_weekend_gap(oj, "Orange Juice (Down)", 0.0, "down", 27.0, None, 5)
        zs = fetch_data("ZS=F")
        if m in [5, 6]: st.write(f"⏭️ Soybeans (Up): Pause im {n}")
        else: check_weekend_gap(zs, "Soybeans (Up)", 0.0, "up", 400.0, None, 17)
        if m in [1, 2, 11, 12]: st.write(f"⏭️ Soybeans (Down): Pause im {n}")
        else: check_weekend_gap(zs, "Soybeans (Down)", 5.0, "down", 220.0, 260.0, 14)
        check_weekend_gap(fetch_data("ZW=F"), "Wheat", 5.0, "down", 240.0, 320.0, 20)
