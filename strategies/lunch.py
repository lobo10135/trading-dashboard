import yfinance as yf
import pandas as pd
from datetime import datetime

def check_gbp_lunch_momentum(ticker="GBPUSD=X"):
    # Wochentag prüfen: 0=Montag, 1=Dienstag, 2=Mittwoch
    today = datetime.now().weekday()
    
    print("=================================================================")
    print("      GBP Lunch Time by Lobo10135       ")
    print("=================================================================")
    
    # Wochentags-Filter (Mo-Mi aktiv)
    if today not in [0, 1, 2]:
        print(f"Heute ist {datetime.now().strftime('%A')}. Die Strategie ist heute inaktiv (Mo-Mi).")
        return False

    # Daten laden
    data = yf.Ticker(ticker).history(period="10d")
    
    if len(data) < 3:
        print("Nicht genügend Daten für die Momentum-Berechnung verfügbar.")
        return False

    # Schlusskurse extrahieren
    close_yesterday = data['Close'].iloc[-1]
    close_day_before = data['Close'].iloc[-2]
    
    # Aktuellen Kurs holen (falls Markt offen, sonst letzter Schlusskurs)
    current_price = yf.Ticker(ticker).info.get('regularMarketPrice') or data['Close'].iloc[-1]
    
    # Wochentage für die Anzeige
    day_yesterday = data.index[-1].strftime('%A')
    day_before = data.index[-2].strftime('%A')
    
    # Momentum Berechnung
    momentum = (close_yesterday / close_day_before)
    momentum_percent = momentum * 100
    
    print(f"Schlusskurs Vorgestern ({day_before}): {close_day_before:.5f}")
    print(f"Schlusskurs Gestern    ({day_yesterday}): {close_yesterday:.5f}")
    print(f"Momentum:               {momentum_percent:.2f}%")
    
    # Check Bedingung < 99.5%
    if momentum < 0.995:
        print("✅ Bedingung erfüllt: Momentum ist um mehr als 0,5% gefallen.")
        
        # Berechnung: 1 Tick = 0.0001
        stop_kurs = current_price - 0.0110
        take_profit = current_price + 0.0040
        
        print(f"Aktueller Kurs:         {current_price:.5f}")
        print(f"Stopkurs:               {stop_kurs:.5f}")
        print(f"Take Profit 75%:        {take_profit:.5f}")
        return True
    else:
        print("❌ Bedingung nicht erfüllt: Momentum-Rückgang zu gering.")
        return False

if __name__ == "__main__":
    check_gbp_lunch_momentum()
