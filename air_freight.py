import random

def calculate_air_freight(origin, destination, weight, volume, cargo_value, target_currency, fx_rate, currency_symbol):
    print(f"✈️ [Air Engine] Processing Aviation Rules for Route: {origin} ➡️ {destination}")
    
    try:
        w_num = float(weight) if weight else 0
        v_num = float(volume) if volume else 0
        val_num = float(cargo_value) if cargo_value else 0
    except:
        w_num, v_num, val_num = 100, 1, 0

    base_carriers = ["Emirates SkyCargo", "Qatar Cargo", "EgyptAir Cargo", "Saudia Cargo", "Lufthansa Cargo", "DHL Aviation"]
    random.shuffle(base_carriers)
    carriers = base_carriers[:5]
    
    # حساب الوزن الخاضع للأجور (Chargeable Weight)
    chargeable_weight = max(w_num, v_num * 167)
    base_rate_usd = round(random.uniform(1.8, 2.5), 2)
    
    final_rows = []
    for i, carrier in enumerate(carriers):
        single_air_usd = base_rate_usd + i * 0.35
        p_raw_usd = (chargeable_weight * single_air_usd) + 120
        
        # حساب التأمين CIF + 10%
        cif_usd = val_num + p_raw_usd
        ins_usd = max(50.0, (cif_usd * 1.10) * 0.003) if val_num > 0 else 0.0
        
        # تحويل العملة
        p_final = round(p_raw_usd / fx_rate, 2) if target_currency == "EUR" else round(p_raw_usd, 2)
        ins_final = round(ins_usd / fx_rate, 2) if target_currency == "EUR" else round(ins_usd, 2)
        rate_unit_final = round(single_air_usd / fx_rate, 2) if target_currency == "EUR" else round(single_air_usd, 2)
        
        final_rows.append({
            "Carrier / Line Name": carrier,
            f"20FT Rate ({target_currency})": "-",
            f"40HC Rate ({target_currency})": "-",
            f"Loose Unit Rate ({target_currency})": f"{currency_symbol}{rate_unit_final}/KG",
            f"Total Freight Cost ({target_currency})": f"{currency_symbol}{p_final}",
            f"Cargo Insurance ({target_currency})": f"{currency_symbol}{ins_final}" if ins_final > 0 else f"{currency_symbol}0.00",
            "Transit Duration": f"{1 + i}-{2 + i} Days",
            "Shipping Mode": "Air Freight",
            "Origin Code": origin,
            "Destination Code": destination,
            "Total Shipment Weight (KG)": str(w_num),
            "Qty 20FT": "0",
            "Qty 40FT": "0",
            "Schedules Window": "Standard Flight Schedule"
        })
    return final_rows

