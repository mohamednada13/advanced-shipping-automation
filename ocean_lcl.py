import random

def calculate_ocean_lcl(origin, destination, weight, volume, target_currency, fx_rate, currency_symbol, base_date, carrier, i):
    w_num = float(weight) if weight else 0
    v_num = float(volume) if volume else 0
    
    single_lcl_usd = random.randint(45, 65) + (i * 8)
    chargeable_volume = max(v_num, w_num / 1000)
    p_raw_usd = (chargeable_volume * single_lcl_usd) + 90
    rlcl_fin = round(single_lcl_usd / fx_rate, 2) if target_currency == "EUR" else round(single_lcl_usd, 2)
    
    from datetime import timedelta
    sailing_date = (base_date + timedelta(days=random.randint(2, 7))).strftime("%Y-%m-%d")
    
    return {
        "Carrier / Line Name": carrier,
        "Port of Loading (POL)": origin,
        "Port of Discharge (POD)": destination,
        "Total Weight (KG)": str(w_num),
        "Total Volume (CBM)": str(v_num),
        f"LCL Rate ({target_currency}/CBM)": f"{currency_symbol}{rlcl_fin}",
        f"Total Freight Cost ({target_currency})": p_raw_usd, # سنترك الرقم خام ليقوم المدير بحساب التأمين الكلي له
        "Transit Duration": f"{12 + i}-{16 + i} Days",
        "Shipping Mode": "Ocean Freight (LCL)",
        "Vessel Sailing Date": sailing_date
    }
  
