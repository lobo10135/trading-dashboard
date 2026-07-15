import streamlit as st
import yfinance as yf
import datetime
import os

# Seiten-Konfiguration
st.set_page_config(page_title="Gap and Go Weekly", layout="wide")

# Zentrierung exakt wie im GBP Lunch Time Skript [1, 2, 1]
_, col_center, _ = st.columns([1, 2, 1])

def check_weekend_gap(hist, market_name, min_gap_percent=0.0, gap_type="up", stop_distance=None, take_profit_distance=None, holding_weeks=None):
    if hist is None or hist.empty or len(hist) < 2:
        return f"Fehler: Keine ausreichenden Daten für {market_name} verfügbar."

    vorwoche_data = None
    neuwoche_data = None

    for i in range(len(hist) - 1, 0, -1):
        aktueller_tag = hist.index[i]
        vorheriger_tag = hist.index[i - 1]
        if (aktueller_tag.date() - vorheriger_tag.date()).days >= 2:
            neuwoche_data = hist.iloc[i]
            vorwoche_data = hist.iloc[i - 1]
            break

    if vorwoche_data is None or neuwoche_data is None:
        neuwoche_data = hist.iloc[-1]
        vorwoche_data = hist.iloc[-2]

    neuwoche_open = float(neuwoche_data["Open"])
    datum_vorwoche = vorwoche_data.name.strftime("%d.%m.%Y")
    datum_neuwoche = neuwoche_data.name.strftime("%d.%m.%Y")
    wochentag_name = ("Sonntag" if neuwoche_data.name.weekday() == 6 else "Montag")

    def get_exit_friday(start_date, weeks):
        target_date = start_date.date() + datetime.timedelta(weeks=weeks)
        current_weekday = target_date.weekday()
        days_to_friday = 4 - current_weekday if current_weekday <= 4 else 4 - current_weekday + 7
        exit_date = target_date + datetime.timedelta(days=days_to_friday)
        return exit_date.strftime("%d.%m.%Y")

    output = []
    if gap_type == "up":
        vorwoche_high = float(vorwoche_data["High"])
        gap_punkte = neuwoche_open - vorwoche_high
        gap_prozent = (gap_punkte / vorwoche_high) * 100
        is_gap = gap_punkte > 0 and gap_prozent > min_gap_percent

        if is_gap:
            output.append("=" * 50)
            output.append(f" 🟢 {market_name.upper()} UP-GAP GEFUNDEN (> {min_gap_percent}%) ")
            output.append("=" * 50)
            output.append(f"Letztes High ({datum_vorwoche}):  {vorwoche_high:.4f} Punkte")
            output.append(f"Eröffnung   ({datum_neuwoche}, {wochentag_name}):  {neuwoche_open:.4f} Punkte")
            output.append("-" * 50)
            output.append(f"Kurslücke nach oben:  +{gap_punkte:.4f} Punkte (+{gap_prozent:.2f}%)")
            if stop_distance: output.append(f"Stop Kurs:           {neuwoche_open - stop_distance:.4f} Punkte")
            if take_profit_distance: output.append(f"Take Profit:         {neuwoche_open + take_profit_distance:.4f} Punkte")
            if holding_weeks: output.append(f"Haltedauer:          {holding_weeks} Wochen (Exit: {get_exit_friday(neuwoche_data.name, holding_weeks)})")
            output.append("=" * 50 + "\n")
        else:
            output.append(f"ℹ️ {market_name}: Kein Up-Gap > {min_gap_percent}% vorhanden (Aktuell: {gap_prozent:+.2f}%).\n")
    else:
        vorwoche_low = float(vorwoche_data["Low"])
        gap_punkte = vorwoche_low - neuwoche_open
        gap_prozent = abs((gap_punkte / vorwoche_low) * 100)
        is_gap = (neuwoche_open < vorwoche_low) and (gap_prozent > min_gap_percent)

        if is_gap:
            output.append("=" * 50)
            output.append(f" 🔴 {market_name.upper()} DOWN-GAP GEFUNDEN (> {min_gap_percent}%) ")
            output.append("=" * 50)
            output.append(f"Letztes Low ({datum_vorwoche}):  {vorwoche_low:.4f} Punkte")
            output.append(f"Eröffnung   ({datum_neuwoche}, {wochentag_name}):  {neuwoche_open:.4f} Punkte")
            output.append("-" * 50)
            output.append(f"Kurslücke nach unten: -{gap_punkte:.4f} Punkte (-{gap_prozent:.2f}%)")
            if stop_distance: output.append(f"Stop Kurs:           {neuwoche_open + stop_distance:.4f} Punkte")
            if take_profit_distance: output.append(f"Take Profit:         {neuwoche_open - take_profit_distance:.4f} Punkte")
            if holding_weeks: output.append(f"Haltedauer:          {holding_weeks} Wochen (Exit: {get_exit_friday(neuwoche_data.name, holding_weeks)})")
            output.append("=" * 50 + "\n")
        else:
            output.append(f"ℹ️ {market_name}: Kein Down-Gap > {min_gap_percent}% vorhanden (Aktuell: -{gap_prozent:.2f}%).\n")
    return "\n".join(output)

def fetch_data(ticker_symbol):
    try:
        asset = yf.Ticker(ticker_symbol)
        hist = asset.history(period="10d")
        return hist if not hist.empty else None
    except: return None

with col_center:
    # Einheitliche Darstellung wie im GBP Lunch Time Skript
    if os.path.exists("bulle.jpg"):
        st.image("bulle.jpg", use_container_width=True)

    # Titel mit Schuh-Icon (👟)
    st.markdown("### 👟 Gap and Go Weekly")
    
    if st.button("Analyse starten"):
        res = []
        m = datetime.datetime.now().month
        n = datetime.datetime.now().strftime("%B")
        
        res.append(check_weekend_gap(fetch_data("^GDAXI"), "DAX 40", 0.0, "up", 1800.0, holding_weeks=11))
        
        if m in [1, 8]: res.append(f"⏭️ EuroStoxx 50: Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(fetch_data("^STOXX50E"), "EuroStoxx 50", 0.0, "up", 240.0, holding_weeks=8))
        
        res.append(check_weekend_gap(fetch_data("ES=F"), "S&P 500 E-Mini Future", 0.0, "up", 300.0, 600.0, 10))
        res.append(check_weekend_gap(fetch_data("^NDX"), "Nasdaq 100", 5.0, "up", 1250.0, 1500.0, 15))
        
        rut = fetch_data("^RUT")
        res.append(check_weekend_gap(rut, "Russell 2000 (Up)", 0.0, "up", 340.0, 200.0, 10))
        if m in [7, 8]: res.append(f"⏭️ Russell 2000 (Down): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(rut, "Russell 2000 (Down)", 10.0, "down", 200.0, 240.0, 0))
        
        dji = fetch_data("^DJI")
        if m in [1, 7]: res.append(f"⏭️ Dow Jones Index (Up): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(dji, "Dow Jones Index (Up)", 0.0, "up", 5000.0, holding_weeks=10))
        if m in [7, 8]: res.append(f"⏭️ Dow Jones Index (Down): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(dji, "Dow Jones Index (Down)", 0.0, "down", 3800.0, 3000.0, 0))
        
        if m in [2, 3]: res.append(f"⏭️ T-Bond: Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(fetch_data("ZB=F"), "US 30Y T-Bond Future (Up)", 0.0, "up", 11.0, 28.0, 11))
        if m in [2, 3]: res.append(f"⏭️ T-Note: Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(fetch_data("ZN=F"), "US 10Y T-Note Future (Up)", 0.0, "up", 8.0, holding_weeks=11))
        
        res.append(check_weekend_gap(fetch_data("EUN3.DE"), "Bund Future", 5.0, "up", 8.0, 16.0, 19))
        if m == 9: res.append(f"⏭️ WTI: Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(fetch_data("CL=F"), "WTI Rohöl", 0.0, "up", 35.0, holding_weeks=16))
        
        rb = fetch_data("RB=F")
        res.append(check_weekend_gap(rb, "Gasoline (Up)", 15.0, "up", 83.33, 83.33, 20))
        if m == 3: res.append(f"⏭️ Gasoline (Down): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(rb, "Gasoline (Down)", 5.0, "down", 38.10, 166.67, 13))
        
        if m in [4, 5, 6]: res.append(f"⏭️ Cotton: Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(fetch_data("CT=F"), "Cotton", 7.0, "up", 17.0, 28.0, 7))
        if m == 7: res.append(f"⏭️ Sugar: Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(fetch_data("SB=F"), "Sugar No.11", 5.0, "up", 358.0, holding_weeks=3))
        
        oj = fetch_data("OJ=F")
        if m in [4, 5, 6, 12]: res.append(f"⏭️ Orange Juice (Up): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(oj, "Orange Juice (Up)", 0.0, "up", 34.0, 187.0, 19))
        if m in [3, 4, 5, 6, 7, 8]: res.append(f"⏭️ Orange Juice (Down): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(oj, "Orange Juice (Down)", 0.0, "down", 27.0, holding_weeks=5))
        
        zs = fetch_data("ZS=F")
        if m in [5, 6]: res.append(f"⏭️ Soybeans (Up): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(zs, "Soybeans (Up)", 0.0, "up", 400.0, holding_weeks=17))
        if m in [1, 2, 11, 12]: res.append(f"⏭️ Soybeans (Down): Nicht im Monat {n} aktiv.\n")
        else: res.append(check_weekend_gap(zs, "Soybeans (Down)", 5.0, "down", 220.0, 260.0, 14))
        
        res.append(check_weekend_gap(fetch_data("ZW=F"), "Wheat (Weizen)", 5.0, "down", 240.0, 320.0, 20))
        
        st.text("\n".join(res))
