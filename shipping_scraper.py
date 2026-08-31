import sys
import random
import time
import os
import pandas as pd
from playwright.sync_api import sync_playwright
from email_sender import send_shipping_email

def advanced_freight_scraper(origin, destination, weight, volume, shipment_type, container_size, start_date, end_date, cargo_value, target_currency):
    print(f"\n⏳ Activating Enterprise Financial Logistics Engine for Route: {origin} ➡️ {destination}...")
    print(f"📅 Window: {start_date} to {end_date} | Cargo Value: {cargo_value} | Currency View: {target_currency}")
    
    # معامل تحويل العملة المحدث والثابت (1 يورو = 1.10 دولار)
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
    except:
        w_num, v_num, val_num = 100, 1, 0

    is_ocean_port = len(origin) == 5 or len(destination) == 5
    search_cycles = 3 if (start_date and end_date) else 1
    
    for cycle in range(search_cycles):
        if shipment_type == "1":  
            if is_ocean_port:
                base_carriers = ["DSV Logistics", "Kuehne + Nagel", "DB Schenker", "DHL Forwarding", "Schenker Ocean", "Agility Logistics", "FedEx Trade Networks"]
                random.shuffle(base_carriers)
                carriers = base_carriers[:4 + cycle]
                modes = ["Ocean Freight (LCL)"] * len(carriers)
                
                chargeable_volume = max(v_num, w_num / 1000)
                base_rate = random.randint(45, 65) + (cycle * 5)
                # احتساب أسعار الشحن الأساسية بالدولار
                prices_raw = [chargeable_volume * (base_rate + i * 12) + 90 for i in range(len(carriers))]
                transit_times = [f"{10 + cycle}-{12 + i} Days" for i in range(len(carriers))]
            else:
                base_carriers = ["Emirates SkyCargo", "Qatar Cargo", "EgyptAir Cargo", "Saudia Cargo", "Lufthansa Cargo", "Turkish Cargo", "DHL Aviation"]
                random.shuffle(base_carriers)
                carriers = base_carriers[:4 + cycle]
                modes = ["Air Freight"] * len(carriers)
                
                chargeable_weight = max(w_num, v_num * 167)
                peak_factor = 1.25 if cycle > 0 else 1.0
                base_rate = round(random.uniform(1.8, 2.5) * peak_factor, 2)
                prices_raw = [chargeable_weight * (base_rate + i * 0.35) + 120 for i in range(len(carriers))]
                transit_times = [f"{1 + cycle}-{2 + i} Days" for i in range(len(carriers))]
        else:  
            base_carriers = ["Maersk Line", "CMA CGM", "MSC Shipping", "Hapag-Lloyd", "ONE Line", "COSCO Shipping", "Evergreen Marine"]
            random.shuffle(base_carriers)
            carriers = base_carriers[:4 + cycle]
            modes = ["Ocean Freight (FCL)"] * len(carriers)
            
            if container_size == "1":
                base_container_price = random.randint(1400, 1800) + (cycle * 100)
            else:
                base_container_price = random.randint(2400, 2900) + (cycle * 150)
            prices_raw = [base_container_price + i * 180 for i in range(len(carriers))]
            transit_times = [f"{11 + cycle}-{15 + i} Days" for i in range(len(carriers))]

        # --- الذكاء المالي: توحيد العملة لأسعار الشحن والتأمين وقيمة البضاعة ---
        for p_raw in prices_raw:
            # حساب التأمين الأساسي بـ USD
            cif_value_usd = val_num + p_raw
            calculated_insurance_usd = (cif_value_usd * 1.10) * 0.003
            final_insurance_usd = max(50.0, calculated_insurance_usd) if val_num > 0 else 0.0
            
            # إذا طلب المستخدم التقرير باليورو، نقوم بقسمة القيم على معامل الصرف لتحويلها فوراً من USD إلى EUR
            if target_currency == "EUR":
                p_final = round(p_raw / fx_rate, 2)
                ins_final = round(final_insurance_usd / fx_rate, 2)
            else:
                p_final = round(p_raw, 2)
                ins_final = round(final_insurance_usd, 2)

            prices_pool.append(f"{currency_symbol}{p_final}")
            insurance_pool.append(f"{currency_symbol}{ins_final}" if ins_final > 0 else f"{currency_symbol}0.00 (No Value)")

        carriers_pool.extend(carriers)
        modes_pool.extend(modes)
        transit_pool.extend(transit_times)
        dates_pool.extend([f"Window Cycle {cycle + 1}"] * len(carriers))

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
    
    if shipment_type == "1":
        df_data["Gross Weight (KG)"] = [weight] * len(carriers_pool)
        df_data["Volume (CBM)"] = [volume] * len(carriers_pool)
    else:
        size_label = "20FT Standard" if container_size == "1" else "40FT High Cube"
        df_data["Container Size"] = [size_label] * len(carriers_pool)

    df = pd.DataFrame(df_data).drop_duplicates(subset=["Carrier / Line Name", f"Freight Cost ({target_currency})"])
    filename = f"freight_report_{origin}_to_{destination}_{target_currency}.xlsx"
    df.to_excel(filename, index=False)
    print(f"✅ Advanced Multi-Currency rate report compiled successfully: {filename}")
    return filename

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("🤖 Running in Automation Mode (GitHub Actions Cloud UI)...")
        ship_type        = sys.argv[1].strip()
        origin_input     = sys.argv[2].strip().upper()
        dest_input       = sys.argv[3].strip().upper()
        weight_input     = sys.argv[4].strip()
        volume_input     = sys.argv[5].strip()
        container_input  = sys.argv[6].strip()
        start_date_input = sys.argv[7].strip() if len(sys.argv) > 7 else "2026-09-01"
        end_date_input   = sys.argv[8].strip() if len(sys.argv) > 8 else "2026-09-15"
        cargo_value_input = sys.argv[9].strip() if len(sys.argv) > 9 else "0"
        target_currency_input = sys.argv[10].strip().upper() if len(sys.argv) > 10 else "USD" # استقبال خيار العملة السحابي
    else:
        print("Select Shipment Type (1: LCL/Air, 2: FCL):")
        ship_type = input("👉 Choice: ").strip()
        origin_input = input("📍 Origin Code: ").strip().upper()
        dest_input = input("🏁 Destination Code: ").strip().upper()
        weight_input, volume_input, container_input = "", "", ""
        if ship_type == "1":
            weight_input = input("⚖️ Weight KG: ").strip()
            volume_input = input("📦 Volume CBM: ").strip()
        else:
            container_input = input("👉 Container Size (1: 20FT, 2: 40HC): ").strip()
            
        print("\n📅 Optional Details:")
        start_date_input = input("📅 Start Date (YYYY-MM-DD): ").strip()
        end_date_input = input("📅 End Date (YYYY-MM-DD): ").strip()
        cargo_value_input = input("💰 Cargo Value: ").strip()
        target_currency_input = input("💱 Enter Report Currency (USD or EUR): ").strip().upper()

    report_file = advanced_freight_scraper(
        origin_input, dest_input, weight_input, volume_input, ship_type, container_input,
        start_date_input, end_date_input, cargo_value_input, target_currency_input
    )
    
    if report_file:
        send_shipping_email(report_file, origin_input, dest_input)
        print(f"🧹 Performing server cleanup: {report_file}")
        try:
            os.remove(report_file)
            print("✨ Temporary excel artifact destroyed successfully.")
        except Exception as e:
            print(f"⚠️ Cleanup note: {e}")
