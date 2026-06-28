import streamlit as st
import yfinance as yf
import datetime
from datetime import datetime as dt
import bs4 as bs
import pandas as pd
import requests
from fpdf import FPDF

# --- Konfiguration ---
st.set_page_config(page_title="Trading Dashboard", page_icon="📈")

# Bild anstelle des Titels eingefügt
st.image("bulle.jpg", use_container_width=True)

st.markdown("""
    <style>
    button, [data-baseweb="select"], [data-baseweb="select"] *, div[role="combobox"], input {
        cursor: default !important;
    }
    </style>
""", unsafe_allow_html=True)

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
            st.success(f"🟢 {market_name.upper()} UP-GAP")
            st.write(f"Gap: +{gap_punkte:.4f} (+{gap_prozent:.2f}%)")
            if stop_distance: st.write(f"Stop: {neuwoche_open - stop_distance:.4f}")
            if take_profit_distance: st.write(f"TP: {neuwoche_open + take_profit_distance:.4f}")
            if holding_weeks: st.write(f"Haltedauer: {holding_weeks} Wochen (Exit: {get_exit_friday(neuwoche_data.name, holding_weeks)})")
        else: st.info(f"ℹ️ {market_name}: Kein Up-Gap > {min_gap_percent}%")

    elif gap_type == "down":
        vorwoche_low = float(vorwoche_data["Low"])
        gap_punkte = vorwoche_low - neuwoche_open
        gap_prozent = abs((gap_punkte / vorwoche_low) * 100)
        if (neuwoche_open < vorwoche_low) and (gap_prozent > min_gap_percent):
            st.error(f"🔴 {market_name.upper()} DOWN-GAP")
            st.write(f"Gap: -{gap_punkte:.4f} (-{gap_prozent:.2f}%)")
            if stop_distance: st.write(f"Stop: {neuwoche_open + stop_distance:.4f}")
            if take_profit_distance: st.write(f"TP: {neuwoche_open - take_profit_distance:.4f}")
            if holding_weeks: st.write(f"Haltedauer: {holding_weeks} Wochen (Exit: {get_exit_friday(neuwoche_data.name, holding_weeks)})")
        else: st.info(f"ℹ️ {market_name}: Kein Down-Gap > {min_gap_percent}%")

def fetch_data(ticker_symbol):
    try:
        hist = yf.Ticker(ticker_symbol).history(period="10d")
        return hist if not hist.empty else None
    except: return None

# --- Strategie 3: RSL Analyse ---
def create_pdf(top, flop):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    def write_data(pdf_obj, df, title):
        pdf_obj.set_font("Arial", 'B', 14)
        pdf_obj.cell(200, 10, txt=title, ln=True)
        pdf_obj.set_font("Courier", '', 8)
        header = f"{'Rang':^8} {'Ticker':<10} {'Name':<25} {'Kurs':<12} {'RSL':<12}"
        pdf_obj.cell(200, 5, txt=header, ln=True)
        pdf_obj.cell(200, 1, txt="-"*67, ln=True)
        for _, row in df.iterrows():
            name = str(row['Name'])[:22]
            line = f"{str(row['Rang']):^8} {str(row['Ticker']):<10} {name:<25} {str(row['Aktueller_Kurs']):<12} {str(row['RSL_26W']):<12}"
            line = line.encode('ascii', 'replace').decode('ascii')
            pdf_obj.cell(200, 5, txt=line, ln=True)
        pdf_obj.ln(10)

    write_data(pdf, top, "TOP 125 Aktien")
    pdf.add_page()
    write_data(pdf, flop, "FLOP 125 Aktien")
    return pdf.output(dest='S').encode('latin-1')

def clean_sector_name(raw_sector):
    if "Discretionary" in raw_sector: return "Consumer-Disc"
    if "Staples" in raw_sector: return "Consumer-Stap"
    return raw_sector.split()[0]

def get_sp500_data_from_wikipedia():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"id": "constituents"})
    ticker_info_map = {}
    for row in table.findAll("tr")[1:]:
        cells = row.findAll("td")
        ticker = cells[0].text.strip().replace(".", "-")
        ticker_info_map[ticker] = {"Name": cells[1].text.strip(), "Sektor": clean_sector_name(cells[3].text.strip())}
    return ticker_info_map

def calculate_rsl_26_weeks():
    try:
        ticker_info_map = get_sp500_data_from_wikipedia()
        tickers = list(ticker_info_map.keys())
    except: return pd.DataFrame(), pd.DataFrame()

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=240)
    raw_data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
    
    rsl_results = []
    window = 130
    for ticker in tickers:
        if ticker in raw_data.columns:
            series = raw_data[ticker].dropna()
            if len(series) >= window:
                rsl = series.iloc[-1] / series.iloc[-window:].mean()
                info = ticker_info_map.get(ticker, {"Name": "U", "Sektor": "U"})
                rsl_results.append({"Ticker": ticker, "Name": info["Name"], "Sektor": info["Sektor"], "Aktueller_Kurs": round(float(series.iloc[-1]), 2), "RSL_26W": round(float(rsl), 4)})

    df = pd.DataFrame(rsl_results).sort_values(by="RSL_26W", ascending=False).reset_index(drop=True)
    
    top_125 = df.head(125).copy()
    top_125.insert(0, "Rang", [str(i) for i in range(1, len(top_125) + 1)])
    
    flop_125 = df.tail(125).sort_values(by="RSL_26W", ascending=True).copy()
    flop_125.insert(0, "Rang",
