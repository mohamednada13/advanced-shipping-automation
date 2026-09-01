import random
from datetime import datetime

from ocean_lcl import calculate_ocean_lcl
from ocean_fcl import calculate_ocean_fcl
from ocean_hybrid import calculate_ocean_hybrid

def calculate_ocean_freight(origin, destination, weight, volume, count_20ft, count_40ft, shipment_type, cargo_value, target_currency, fx_rate, currency_symbol, start_date):
    if len(origin) != 5 or len(destination) != 5:
        raise ValueError("❌ [Ocean Error] Maritime port codes must be strictly 5 characters (UN/LOCODE standard).")
        
    try:
        val_num = float(cargo_value) if cargo_value else 0
        v_num = float(volume) if volume else 0
        c20 = int(count_20ft) if count_20ft else 0
        c40 = int(count_40ft) if count_40ft else 0
    except:
        val_num, v_num, c20, c40 = 0, 0, 0, 0

    base_carriers = ["Maersk Line", "CMA CGM", "MSC Shipping", "Hapag-Lloyd", "ONE Line", "COSCO Shipping", "Evergreen Marine", "HMM Shipping"]
    random.shuffle(base_carriers)
    carriers = base_carriers[:6]
    
    try:
        base_date = datetime.strptime(start_date, "%Y-%m-%d")
    except:
        base_date = datetime.now()

    final_rows = []
    for i, carrier in enumerate(carriers):
        if shipment_type == "1":
            row = calculate_ocean_lcl(origin, destination, weight, volume, target_currency, fx_rate, currency_symbol, base_date, carrier, i)
        elif (c20 > 0 or c40 > 0) and v_num > 0:
            row = calculate_ocean_hybrid(origin, destination, weight, volume, count_20ft, count_40ft, target_currency, fx_rate, currency_symbol, base_date, carrier, i)
        else:
            row = calculate_ocean_fcl(origin, destination, weight, count_20ft, count_40ft, target_currency, fx_rate, currency_symbol, base_date, carrier, i)
            
        p_raw_usd = row[f"Total Freight Cost ({target_currency})"]
        cif_usd = val_num + p_raw_usd
        ins_usd = max(50.0, (cif_usd * 1.10) * 0.003) if val_num > 0 else 0.0
        
        p_final = round(p_raw_usd / fx_rate, 2) if target_currency == "EUR" else round(p_raw_usd, 2)
        ins_final = round(ins_usd / fx_rate, 2) if target_currency == "EUR" else round(ins_usd, 2)
        
        row[f"Total Freight Cost ({target_currency})"] = f"{currency_symbol}{p_final}"
        row[f"Cargo Insurance ({target_currency})"] = f"{currency_symbol}{ins_final}" if ins_final > 0 else f"{currency_symbol}0.00"
        
        final_rows.append(row)
    return final_rows
