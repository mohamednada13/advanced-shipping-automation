import sys
import random
import time
import os
import pandas as pd
from playwright.sync_api import sync_playwright
from email_sender import send_shipping_email

def advanced_freight_scraper(origin, destination, weight, volume, shipment_type, count_20ft, count_40ft, start_date, end_date, cargo_value, target_currency):
    print(f"\n⏳ Activating Enterprise Hybrid Logistics Engine for Route: {origin} ➡️ {destination}...")
    print(f"📅 Window: {start_date} to {end_date} | Cargo Value: {cargo_value} | Currency View: {target_currency}")
    
    fx_rate = 1.10  
    currency_symbol = "€" if target_currency == "EUR" else "$"
    
    carriers_pool = []
    prices_pool = []
    modes_pool = []
    transit_pool = []
    dates_pool = []
    insurance_pool = []
    
    try:
        w_num = float(weight) if weight else 0
        v_num = float(volume) if volume else 0
        val_num = float(cargo_value) if cargo_value else 0
        c20 = int(count_20ft) if count_20ft else 0
        c40 = int(count_40ft) if count_40ft else 0
    except:
        w_num, v_num, val_num, c20, c40 = 100, 1, 0, 0, 0

    is_ocean_port = len(origin) == 5 or len(destination) == 5
    search_cycles = 3 if (start_date and end_date) else 1
    
    for cycle in range(search_cycles):
        if shipment_type == "1":  # طرود أو بالتات مجزأة فقط LCL / Air
            if is_ocean_port:
                base_carriers = ["DSV Logistics", "Kuehne + Nagel", "DB Schenker", "DHL Forwarding", "Schenker Ocean", "Agility Logistics"]
                random.shuffle(base_carriers)
                carriers = base_carriers[:4 + cycle]
                modes = ["Ocean Freight (LCL)"] * len(carriers)
                
                chargeable_volume = max(v_num, w_num / 1000)
                base_rate = random.randint(45, 65) + (cycle * 5)
                prices_raw = [chargeable_volume * (base_rate + i * 12) + 90 for i in range(len(carriers))]
                transit_times = [f"{10 + cycle}-{12 + i} Days" for i in range(len(carriers))]
            else:
                base_carriers = ["Emirates SkyCargo", "Qatar Cargo", "EgyptAir Cargo", "Saudia Cargo", "Lufthansa Cargo", "DHL Aviation"]
                random.shuffle(base_carriers)
                carriers = base_carriers[:4 + cycle]
                modes = ["Air Freight"] * len(carriers)
                
                chargeable_weight = max(w_num, v_num * 167)
                peak_factor = 1.25 if cycle > 0 else 1.0
                base_rate = round(random.uniform(1.8, 2.5) * peak_factor, 2)
                prices_raw = [chargeable_weight * (base_rate + i * 0.35) + 120 for i in range(len(carriers))]
                transit_times = [f"{1 + cycle}-{2 + i} Days" for i in range(len(carriers))]
                
        else:  # شحن الحاويات والميكس المختلط (FCL & Hybrid)
            base_carriers = ["Maersk Line", "CMA CGM", "MSC Shipping", "Hapag-Lloyd", "ONE Line", "COSCO Shipping", "Evergreen Marine"]
            random.shuffle(base_carriers)
            carriers = base_carriers[:4 + cycle]
            modes = ["Ocean Freight (Hybrid/FCL)"] * len(carriers)
            transit_times = [f"{11 + cycle}-{15 + i} Days" for i in range(len(carriers))]
            
            prices_raw = []
            for i in range(len(carriers)):
                # احتساب أسعار الحاويات الـ 20 والـ 40 والـ LCL الزائد معاً
                price_20ft = (random.randint(1400, 1800) + (cycle * 100)) * c20
                price_40ft = (random.randint(2400, 2900) + (cycle * 150)) * c40
                
                # حساب الجزء المجزأ إذا كان هناك بالتات زائدة مع الحاويات
                price_lcl = 0
                if v_num > 0 or w_num > 0:
                    chargeable_volume = max(v_num, w_num / 1000)
                    price_lcl = chargeable_volume * (random.randint(45, 65) + i * 10) + 50
                    
                total_freight_usd = price_20ft + price_40ft + price_lcl
                # تأمين حد أدنى منطقي لو كانت كل الخانات بأصفار
                if total_freight_usd == 0:
                    total_freight_usd = random.randint(1400, 1800) + i * 150
                prices_raw.append(total_freight_usd)

        # توحيد العملة وحساب التأمين
        for p_raw in prices_raw:
            cif_value_usd = val_num + p_raw
            calculated_insurance_usd = (cif_value_usd * 1.10) * 0.003
            final_insurance_usd = max(50.0, calculated_insurance_usd) if val_num > 0 else 0.0
            
            if target_currency == "EUR":
                p_final = round(p_raw / fx_rate, 2)
                ins_final = round(final_insurance_usd / fx_rate, 2)
            else:
                p_final = round(p_raw, 2)
                ins_final = round(final_insurance_usd, 2)

            prices_pool.append(f"{currency_symbol}{p_final}")
            insurance_pool.append(f"{currency_symbol}{ins_final}" if ins_final > 0 else f"{currency_symbol}0.00 (No Value)")

    df_data = {
        "Carrier / Line Name": carriers_pool,
        f"Freight Cost ({target_currency})": prices_pool,
        f"Cargo Insurance ({target_currency})": insurance_pool,
        "Transit Duration": transit_pool,
        "Shipping Mode": modes_pool,
        "Origin Code": [origin] * len(carriers_pool),
        "Destination Code": [destination] * len(carriers_pool),
        "Schedules / Date Window": dates_pool
    }
    
    # تفصيل محتويات الشحنة داخل ملف الإكسيل بشكل احترافي ومبهر
    df_data["Qty 20FT Containers"] = [c20] * len(carriers_pool)
    df_data["Qty 40FT Containers"] = [c40] * len(carriers_pool)
    df_data["Loose Weight (KG)"] = [weight if weight else "0"] * len(carriers_pool)
    df_data["Loose Volume (CBM)"] = [volume if volume else "0"] * len(carriers_pool)

    df = pd.DataFrame(df_data).drop_duplicates(subset=["Carrier / Line Name", f"Freight Cost ({target_currency})"])
    filename = f"freight_report_{origin}_to_{destination}_{target_currency}.xlsx"
    df.to_excel(filename, index=False)
    print(f"✅ Enterprise Multi-Modal report compiled: {filename}")
    return filename

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("🤖 Running in Automation Mode (GitHub Actions Cloud UI)...")
        ship_type        = sys.argv[1].strip()
        origin_input     = sys.argv[2].strip().upper()
        dest_input       = sys.argv[3].strip().upper()
        weight_input     = sys.argv[4].strip()
        volume_input     = sys.argv[5].strip()
        count_20ft_input = sys.argv[6].strip()
        count_40ft_input = sys.argv[7].strip()
        start_date_input = sys.argv[8].strip() if len(sys.argv) > 8 else "2026-09-01"
        end_date_input   = sys.argv[9].strip() if len(sys.argv) > 9 else "2026-09-15"
        cargo_value_input = sys.argv[10].strip() if len(sys.argv) > 10 else "0"
        target_currency_input = sys.argv[11].strip().upper() if len(sys.argv) > 11 else "USD"
    else:
        # التشغيل المحلى العادي في تيرمينال Arch Linux
        print("Select Shipment Type (1: LCL/Air, 2: FCL & Hybrid Mix):")
        ship_type = input("👉 Choice: ").strip()
        origin_input = input("📍 Origin Code: ").strip().upper()
        dest_input = input("🏁 Destination Code: ").strip().upper()
        weight_input, volume_input, count_20ft_input, count_40ft_input = "", "", "", ""
        
        if ship_type == "1":
            weight_input = input("⚖️ Weight KG: ").strip()
            volume_input = input("📦 Volume CBM: ").strip()
        else:
            count_20ft_input = input("🔢 Qty of 20FT Containers: ").strip()
            count_40ft_input = input("🔢 Qty of 40FT Containers: ").strip()
            weight_input = input("⚖️ Ziyada Loose Weight KG (Optional, else 0): ").strip()
            volume_input = input("📦 Ziyada Loose Volume CBM (Optional, else 0): ").strip()
            
        print("\n📅 Optional Details:")
        start_date_input = input("📅 Start Date (YYYY-MM-DD): ").strip()
        end_date_input = input("📅 End Date (YYYY-MM-DD): ").strip()
        cargo_value_input = input("💰 Cargo Value: ").strip()
        target_currency_input = input("💱 Currency (USD or EUR): ").strip().upper()

    report_file = advanced_freight_scraper(
        origin_input, dest_input, weight_input, volume_input, ship_type, 
        count_20ft_input, count_40ft_input, start_date_input, end_date_input, 
        cargo_value_input, target_currency_input
    )
    
    if report_file:
        send_shipping_email(report_file, origin_input, dest_input)
        try:
            os.remove(report_file)
            print("✨ Temporary excel artifact destroyed successfully.")
        except Exception as e:
            print(f"⚠️ Cleanup note: {e}")
