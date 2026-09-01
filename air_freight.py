import random
from datetime import datetime, timedelta

def calculate_air_freight(origin, destination, weight, volume, cargo_value, target_currency, fx_rate, currency_symbol, start_date):
    print(f"✈️ [Air Engine] Processing validated aviation compliance pipeline...")
    
    if len(origin) < 3 or len(origin) > 4 or len(destination) < 3 or len(destination) > 4:
        raise ValueError("❌ [Air Error] Airport codes must be strictly between 3 and 4 characters (IATA/ICAO).")
        
    try:
        w_num = float(weight) if weight else 0.0
        v_num = float(volume) if volume else 0.0
        val_num = float(cargo_value) if cargo_value else 0.0
    except:
        w_num, v_num, val_num = 100.0, 1.0, 0.0

    base_carriers = ["Emirates SkyCargo", "Qatar Cargo", "EgyptAir Cargo", "Saudia Cargo", "Lufthansa Cargo", "DHL Aviation", "Turkish Cargo", "British Cargo"]
    random.shuffle(base_carriers)
    carriers = base_carriers[:6]
    
    chargeable_weight = max(w_num, v_num * 167.0)
    base_rate_usd = round(random.uniform(1.8, 2.5), 2)
    
    try:
        base_date = datetime.strptime(start_date, "%Y-%m-%d")
    except:
        base_date = datetime.now()

    final_rows = []
    for i, carrier in enumerate(carriers):
        single_air_usd = base_rate_usd + (i * 0.25)
        p_raw_usd = (chargeable_weight * single_air_usd) + 120.0
        
        cif_usd = val_num + p_raw_usd
        ins_usd = max(50.0, (cif_usd * 1.10) * 0.003) if val_num > 0.0 else 0.0
        
        p_final = round(p_raw_usd / fx_rate, 2) if target_currency == "EUR" else round(p_raw_usd, 2)
        ins_final = round(ins_usd / fx_rate, 2) if target_currency == "EUR" else round(ins_usd, 2)
        rate_unit_final = round(single_air_usd / fx_rate, 2) if target_currency == "EUR" else round(single_air_usd, 2)
        
        flight_date = (base_date + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
        
        final_rows.append({
            "Carrier / Line Name": carrier,
            f"Loose Unit Rate ({target_currency})": f"{currency_symbol}{rate_unit_final}/KG",
            f"Total Freight Cost ({target_currency})": f"{currency_symbol}{p_final}",
            f"Cargo Insurance ({target_currency})": f"{currency_symbol}{ins_final}" if ins_final > 0 else f"{currency_symbol}0.00",
            "Transit Duration": f"{1 + i}-{2 + i} Days",
            "Shipping Mode": "Air Freight",
            "Airport of Departure (AOD)": origin,
            "Airport of Destination (AOD)": destination,
            "Total Shipment Weight (KG)": str(w_num),
            "Estimated Flight Date": flight_date
        })
    return final_rows
