import random

def calculate_ocean_fcl(origin, destination, weight, count_20ft, count_40ft, target_currency, fx_rate, currency_symbol, base_date, carrier, i):
    w_num = float(weight) if weight else 0
    c20 = int(count_20ft) if count_20ft else 0
    c40 = int(count_40ft) if count_40ft else 0
    
    single_20ft_usd = random.randint(1400, 1800) + (i * 65)
    single_40ft_usd = random.randint(2400, 2900) + (i * 95)
    
    p_raw_usd = (single_20ft_usd * c20) + (single_40ft_usd * c40)
    if p_raw_usd == 0:
        p_raw_usd = single_20ft_usd
        c20 = 1
        
    r20_fin = round(single_20ft_usd / fx_rate, 2) if target_currency == "EUR" else round(single_20ft_usd, 2)
    r40_fin = round(single_40ft_usd / fx_rate, 2) if target_currency == "EUR" else round(single_40ft_usd, 2)
    
    from datetime import timedelta
    sailing_date = (base_date + timedelta(days=random.randint(2, 7))).strftime("%Y-%m-%d")
    
    return {
        "Carrier / Line Name": carrier,
        "Port of Loading (POL)": origin,
        "Port of Discharge (POD)": destination,
        "Total Weight (KG)": str(w_num),
        "Qty 20FT": str(c20),
        "Qty 40FT": str(c40),
        f"20FT Rate ({target_currency})": f"{currency_symbol}{r20_fin}" if c20 > 0 else "-",
        f"40HC Rate ({target_currency})": f"{currency_symbol}{r40_fin}" if c40 > 0 else "-",
        f"Total Freight Cost ({target_currency})": p_raw_usd,
        "Transit Duration": f"{12 + i}-{16 + i} Days",
        "Shipping Mode": "Ocean Freight (FCL)",
        "Vessel Sailing Date": sailing_date
    }
  
