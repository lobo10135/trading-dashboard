import datetime
import yfinance as yf

def check_weekend_gap(
    hist,
    market_name,
    min_gap_percent=0.0,
    gap_type="up",
    stop_distance=None,
    take_profit_distance=None,
    holding_weeks=None,
):
    """Prüft historische Daten auf ein Wochenend-Gap und nutzt Absolutwerte für den Vergleich."""
    if hist is None or hist.empty or len(hist) < 2:
        print(f"Fehler: Keine ausreichenden Daten für {market_name} verfügbar.")
        return

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

    if gap_type == "up":
        vorwoche_high = float(vorwoche_data["High"])
        gap_punkte = neuwoche_open - vorwoche_high
        gap_prozent = (gap_punkte / vorwoche_high) * 100
        is_gap = gap_punkte > 0 and gap_prozent > min_gap_percent

        if is_gap:
            print("=" * 50)
            print(f" 🟢 {market_name.upper()} UP-GAP GEFUNDEN (> {min_gap_percent}%) ")
            print("=" * 50)
            print(f"Letztes High ({datum_vorwoche}):  {vorwoche_high:.4f} Punkte")
            print(f"Eröffnung   ({datum_neuwoche}, {wochentag_name}):  {neuwoche_open:.4f} Punkte")
            print("-" * 50)
            print(f"Kurslücke nach oben:  +{gap_punkte:.4f} Punkte (+{gap_prozent:.2f}%)")
            if stop_distance is not None:
                print(f"Stop Kurs:           {neuwoche_open - stop_distance:.4f} Punkte")
            if take_profit_distance is not None:
                print(f"Take Profit:         {neuwoche_open + take_profit_distance:.4f} Punkte")
            if holding_weeks is not None:
                exit_datum = get_exit_friday(neuwoche_data.name, holding_weeks)
                print(f"Haltedauer:          {holding_weeks} Wochen (Exit: {exit_datum})")
            print("=" * 50 + "\n")
        else:
            print(f"ℹ️ {market_name}: Kein Up-Gap > {min_gap_percent}% vorhanden (Aktuell: {gap_prozent:+.2f}%).\n")

    elif gap_type == "down":
        vorwoche_low = float(vorwoche_data["Low"])
        gap_punkte = vorwoche_low - neuwoche_open
        gap_prozent = abs((gap_punkte / vorwoche_low) * 100)
        is_gap = (neuwoche_open < vorwoche_low) and (gap_prozent > min_gap_percent)

        if is_gap:
            print("=" * 50)
            print(f" 🔴 {market_name.upper()} DOWN-GAP GEFUNDEN (> {min_gap_percent}%) ")
            print("=" * 50)
            print(f"Letztes Low ({datum_vorwoche}):  {vorwoche_low:.4f} Punkte")
            print(f"Eröffnung   ({datum_neuwoche}, {wochentag_name}):  {neuwoche_open:.4f} Punkte")
            print("-" * 50)
            print(f"Kurslücke nach unten: -{gap_punkte:.4f} Punkte (-{gap_prozent:.2f}%)")
            if stop_distance is not None:
                print(f"Stop Kurs:           {neuwoche_open + stop_distance:.4f} Punkte")
            if take_profit_distance is not None:
                print(f"Take Profit:         {neuwoche_open - take_profit_distance:.4f} Punkte")
            if holding_weeks is not None:
                exit_datum = get_exit_friday(neuwoche_data.name, holding_weeks)
                print(f"Haltedauer:          {holding_weeks} Wochen (Exit: {exit_datum})")
            print("=" * 50 + "\n")
        else:
            print(f"ℹ️ {market_name}: Kein Down-Gap > {min_gap_percent}% vorhanden (Aktuell: -{gap_prozent:.2f}%).\n")

def fetch_data(ticker_symbol):
    """Holt Daten."""
    try:
        asset = yf.Ticker(ticker_symbol)
        hist = asset.history(period="10d")
        return hist if not hist.empty else None
    except Exception as e:
        print(f"Fehler bei {ticker_symbol}: {e}")
        return None

def main():
    print("=" * 65)
    print("      INDICES, BONDS & COMMODITIES GAP and Go weekly   ")
    print("=" * 65)
    
    aktueller_monat = datetime.datetime.now().month
    monats_name = datetime.datetime.now().strftime("%B")

    # 1. DAX 40
    check_weekend_gap(fetch_data("^GDAXI"), "DAX 40", min_gap_percent=0.0, gap_type="up", stop_distance=1800.0, holding_weeks=11)
    
    # 2. EuroStoxx 50
    if aktueller_monat in [1, 8]: print(f"⏭️ EuroStoxx 50: Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(fetch_data("^STOXX50E"), "EuroStoxx 50", min_gap_percent=0.0, gap_type="up", stop_distance=240.0, holding_weeks=8)

    # 3. S&P 500 E-Mini Future
    check_weekend_gap(fetch_data("ES=F"), "S&P 500 E-Mini Future", min_gap_percent=0.0, gap_type="up", stop_distance=300.0, take_profit_distance=600.0, holding_weeks=10)

    # 4. Nasdaq 100
    check_weekend_gap(fetch_data("^NDX"), "Nasdaq 100", min_gap_percent=5.0, gap_type="up", stop_distance=1250.0, take_profit_distance=1500.0, holding_weeks=15)

    # 5. & 6. Russell 2000
    rut_data = fetch_data("^RUT")
    check_weekend_gap(rut_data, "Russell 2000 (Up)", min_gap_percent=0.0, gap_type="up", stop_distance=340.0, take_profit_distance=200.0, holding_weeks=10)
    if aktueller_monat in [7, 8]: print(f"⏭️ Russell 2000 (Down): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(rut_data, "Russell 2000 (Down)", min_gap_percent=10.0, gap_type="down", stop_distance=200.0, take_profit_distance=240.0, holding_weeks=0)

    # 7. & 8. Dow Jones
    dji_data = fetch_data("^DJI")
    if aktueller_monat in [1, 7]: print(f"⏭️ Dow Jones Industrial (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(dji_data, "Dow Jones Industrial (Up)", min_gap_percent=0.0, gap_type="up", stop_distance=5000.0, holding_weeks=10)
    if aktueller_monat in [7, 8]: print(f"⏭️ Dow Jones Industrial (Down): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(dji_data, "Dow Jones Industrial (Down)", min_gap_percent=0.0, gap_type="down", stop_distance=3800.0, take_profit_distance=3000.0, holding_weeks=0)

    # 9. T-Bond Future
    if aktueller_monat in [2, 3]: print(f"⏭️ US 30Y T-Bond Future (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(fetch_data("ZB=F"), "US 30Y T-Bond Future (Up)", min_gap_percent=0.0, gap_type="up", stop_distance=11.0, take_profit_distance=28.0, holding_weeks=11)

    # 10. 10Y T-Note Future
    if aktueller_monat in [2, 3]: print(f"⏭️ US 10Y T-Note Future (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(fetch_data("ZN=F"), "US 10Y T-Note Future (Up)", min_gap_percent=0.0, gap_type="up", stop_distance=8.0, holding_weeks=11)

    # 11. Euro-Bund Future
    check_weekend_gap(fetch_data("EUN3.DE"), "Bund Future (ETF EUN3.DE)", min_gap_percent=5.0, gap_type="up", stop_distance=8.0, take_profit_distance=16.0, holding_weeks=19)

    # 12. WTI Rohöl
    if aktueller_monat == 9: print(f"⏭️ WTI Rohöl (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(fetch_data("CL=F"), "WTI Rohöl", min_gap_percent=0.0, gap_type="up", stop_distance=35.0, holding_weeks=16)

    # 13. & 18. Gasoline
    rb_data = fetch_data("RB=F")
    check_weekend_gap(rb_data, "Gasoline Benzin (Up)", min_gap_percent=15.0, gap_type="up", stop_distance=83.33, take_profit_distance=83.33, holding_weeks=20)
    if aktueller_monat == 3: print(f"⏭️ Gasoline Benzin (Down): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(rb_data, "Gasoline Benzin (Down)", min_gap_percent=5.0, gap_type="down", stop_distance=38.10, take_profit_distance=166.67, holding_weeks=13)

    # 14. Cotton
    if aktueller_monat in [4, 5, 6]: print(f"⏭️ Cotton (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(fetch_data("CT=F"), "Cotton", min_gap_percent=7.0, gap_type="up", stop_distance=17.0, take_profit_distance=28.0, holding_weeks=7)

    # 15. Sugar No.11
    if aktueller_monat == 7: print(f"⏭️ Sugar No.11 (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(fetch_data("SB=F"), "Sugar No.11", min_gap_percent=5.0, gap_type="up", stop_distance=358.0, holding_weeks=3)

    # 16. & 21. Orange Juice
    oj_data = fetch_data("OJ=F")
    if aktueller_monat in [4, 5, 6, 12]: print(f"⏭️ Orange Juice (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(oj_data, "Orange Juice (Up)", min_gap_percent=0.0, gap_type="up", stop_distance=34.0, take_profit_distance=187.0, holding_weeks=19)
    if aktueller_monat in [3, 4, 5, 6, 7, 8]: print(f"⏭️ Orange Juice (Down): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(oj_data, "Orange Juice (Down)", min_gap_percent=0.0, gap_type="down", stop_distance=27.0, holding_weeks=5)

    # 17. & 20. Soybeans
    zs_data = fetch_data("ZS=F")
    if aktueller_monat in [5, 6]: print(f"⏭️ Soybeans (Up): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(zs_data, "Soybeans (Up)", min_gap_percent=0.0, gap_type="up", stop_distance=400.0, holding_weeks=17)
    if aktueller_monat in [1, 2, 11, 12]: print(f"⏭️ Soybeans (Down): Überprüfung im {monats_name} deaktiviert (Saisonale Pause).\n")
    else: check_weekend_gap(zs_data, "Soybeans (Down)", min_gap_percent=5.0, gap_type="down", stop_distance=220.0, take_profit_distance=260.0, holding_weeks=14)

    # 19. Wheat
    check_weekend_gap(fetch_data("ZW=F"), "Wheat (Weizen)", min_gap_percent=5.0, gap_type="down", stop_distance=240.0, take_profit_distance=320.0, holding_weeks=20)

if __name__ == "__main__":
    main()
