import streamlit as st
import datetime
import bs4 as bs
import pandas as pd
import requests
import yfinance as yf
from fpdf import FPDF

# --- Konfiguration ---
st.set_page_config(page_title="RSL Analyse", page_icon="📈")

st.markdown("""
    <style>
    button, [data-baseweb="select"], [data-baseweb="select"] *, div[role="combobox"], input {
        cursor: default !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 RSL Analyse (S&P 500)")

# --- PDF Generator ---
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

# --- Funktionen ---
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
    
    # Rang als String, damit Streamlit es standardmäßig mittig/links ausrichtet
    top_125 = df.head(125).copy()
    top_125.insert(0, "Rang", [str(i) for i in range(1, len(top_125) + 1)])
    
    flop_125 = df.tail(125).sort_values(by="RSL_26W", ascending=True).copy()
    flop_125.insert(0, "Rang", [str(i) for i in range(1, len(flop_125) + 1)])
    
    return top_125, flop_125

# --- UI ---
if 'results' not in st.session_state: st.session_state.results = None

if st.button("Analyse starten"):
    with st.spinner("Berechne Daten..."):
        st.session_state.results = calculate_rsl_26_weeks()

if st.session_state.results:
    top, flop = st.session_state.results
    
    st.subheader("TOP 125 Aktien nach RSL (26 Wochen)")
    st.dataframe(top, use_container_width=True, hide_index=True)
    
    st.subheader("FLOP 125 Aktien nach RSL (26 Wochen)")
    st.dataframe(flop, use_container_width=True, hide_index=True)

    if st.radio("Soll die Auswertung als PDF exportiert werden?", ("Nein", "Ja")) == "Ja":
        pdf_bytes = create_pdf(top, flop)
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_bytes,
            file_name="RSL_Analyse.pdf",
            mime="application/pdf"
        )
