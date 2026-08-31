import random

def calculate_ocean_freight(origin, destination, weight, volume, count_20ft, count_40ft, shipment_type, cargo_value, target_currency, fx_rate, currency_symbol):
    print(f"🚢 [Ocean Engine] Processing Maritime Rules for Route: {origin} ➡️ {destination}")
    
    try:
        w_num = float(weight) if weight else 0
        v_num = float(volume) if volume else 0
        val_num = float(cargo_value) if cargo_value else 0
        c20 = int(count_20ft) if count_20ft else 0
        c40 = int(count_40ft) if count_40ft else 0
    except:
        w_num, v_num, val_num, c20, c40 = 100, 1, 0, 0, 0

    base_carriers = ["Maersk Line", "CMA CGM", "MSC Shipping", "Hapag-Lloyd", "ONE Line", "COSCO Shipping", "Evergreen Marine"]
    random.shuffle(base_carriers)
    carriers = base_carriers[:5]
    
    final_rows = []
    for i, carrier in enumerate(carriers):
        # 1. حالة البحري المجزأ الصرف LCL
        if shipment_type == "1":
            single_lcl_usd = random.randint(45, 65) + i * 10
            chargeable_volume = max(v_num, w_num / 1000)
            p_raw_usd = (chargeable_volume * single_lcl_usd) + 90
            
            r20_fin, r40_fin = 0.0, 0.0
            rlcl_fin = round(single_lcl_usd / fx_rate, 2) if target_currency == "EUR" else round(single_lcl_usd, 2)
            mode_label = "Ocean Freight (LCL)"
            
        # 2. حالة الحاويات الكاملة والمختلط FCL / Hybrid Mix
        else:
            single_20ft_usd = random.randint(1400, 1800) + (i * 50)
            single_40ft_usd = random.randint(2400, 2900) + (i * 80)
            single_lcl_usd = random.randint(45, 65) + (i * 5) if (v_num > 0 and c20+c40 > 0) else 0
            
            price_20ft = single_20ft_usd * c20
            price_40ft = single_40ft_usd * c40
            price_lcl = (max(v_num, w_num / 1000) * single_lcl_usd + 50) if single_lcl_usd > 0 else 0
            
            p_raw_usd = price_20ft + price_40ft + price_lcl
            if p_raw_usd == 0:
                p_raw_usd = single_20ft_usd
                single_20ft_usd = p_raw_usd
                
            r20_fin = round(single_20ft_usd / fx_rate, 2) if target_currency == "EUR" else round(single_20ft_usd, 2)
            r40_fin = round(single_40ft_usd / fx_rate, 2) if target_currency == "EUR" else round(single_40ft_usd, 2)
            rlcl_fin = round(single_lcl_usd / fx_rate, 2) if (target_currency == "EUR" and single_lcl_usd > 0) else round(single_lcl_usd, 2)
            mode_label = "Ocean Freight (Hybrid)" if single_lcl_usd > 0 else "Ocean Freight (FCL)"

        # حساب التأمين CIF + 10%
        cif_usd = val_num + p_raw_usd
        ins_usd = max(50.0, (cif_usd * 1.10) * 0.003) if val_num > 0 else 0.0
        
        # تصريف العملة النهائي
        p_final = round(p_raw_usd / fx_rate, 2) if target_currency == "EUR" else round(p_raw_usd, 2)
        ins_final = round(ins_usd / fx_rate, 2) if target_currency == "EUR" else round(ins_usd, 2)
        
        final_rows.append({
            "Carrier / Line Name": carrier,
            f"20FT Rate ({target_currency})": f"{currency_symbol}{r20_fin}" if r20_fin > 0 else "-",
            f"40HC Rate ({target_currency})": f"{currency_symbol}{r40_fin}" if r40_fin > 0 else "-",
            f"Loose Unit Rate ({target_currency})": f"{currency_symbol}{rlcl_fin}/CBM" if rlcl_fin > 0 else "-",
            f"Total Freight Cost ({target_currency})": f"{currency_symbol}{p_final}",
            f"Cargo Insurance ({target_currency})": f"{currency_symbol}{ins_final}" if ins_final > 0 else f"{currency_symbol}0.00",
            "Transit Duration": f"{10 + i}-{14 + i} Days",
            "Shipping Mode": mode_label,
            "Origin Code": origin,
            "Destination Code": destination,
            "Total Shipment Weight (KG)": str(w_num),
            "Qty 20FT": str(c20),
            "Qty 40FT": str(c40),
            "Schedules Window": "Vessel Sailing Window"
        })
    return final_rows

