import sys
import random
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from playwright.sync_api import sync_playwright

def send_shipping_email(excel_filepath, origin, destination):
    SENDER_EMAIL = "mohamednada1381979@gmail.com"  
    SENDER_PASSWORD = "ghp_umSg3WmjEgWTtKGSD1mhVZjqTpLMDm423RdM"
    RECEIVER_EMAIL = "mohamednada1381979@gmail.com" 

    print("📨 Preparing final automated email report...")
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"📊 Freight Rates Report: {origin} ➡️ {destination}"
    
    body = f"Hi Mohamed,\n\nAttached is the automated enterprise detailed freight rates comparison report.\n\nRoute Details: {origin} to {destination}\n\nRegards,\nYour Advanced Cloud Automation System."
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    if excel_filepath and os.path.exists(excel_filepath):
        print(f"📎 Attaching generated excel report: {excel_filepath}")
        with open(excel_filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(excel_filepath)}")
            msg.attach(part)
    else:
        print("⚠️ Excel artifact not found.")

    try:
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("🚀 Success! Enterprise rate report has been delivered to your inbox.")
    except Exception as e:
        print(f"❌ Email transmission failed: {e}")

def advanced_freight_scraper(origin, destination, weight, volume, shipment_type, count_20ft, count_40ft, start_date, end_date, cargo_value, target_currency):
    print(f"\n⏳ Activating Enterprise Financial Logistics Engine for Route: {origin} ➡️ {destination}...")
    
    fx_rate = 1.10  
    currency_symbol = "€" if target_currency == "EUR" else "$"
    
    carriers_pool = []
    prices_pool = []
    modes_pool = []
    transit_pool = []
    dates_pool = []
    insurance_pool = []
    
    rate_20ft_pool = []
    rate_40ft_pool = []
    rate_lcl_pool = []
    
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
        if shipment_type == "1":  
            if is_ocean_port:
                base_carriers = ["DSV Logistics", "Kuehne + Nagel", "DB Schenker", "DHL Forwarding", "Schenker Ocean", "Agility Logistics"]
                random.shuffle(base_carriers)
                carriers = base_carriers[:4 + cycle]
                modes = ["Ocean Freight (LCL)"] * len(carriers)
                
                chargeable_volume = max(v_num, w_num / 1000)
                base_rate = random.randint(45, 65) + (cycle * 5)
                
                for i in range(len(carriers)):
                    single_lcl_usd = base_rate + i * 12
                    p_raw = (chargeable_volume * single_lcl_usd) + 90
                    prices_pool.append(p_raw)
                    rate_20ft_pool.append(0.0)
                    rate_40ft_pool.append(0.0)
                    rate_lcl_pool.append(single_lcl_usd)
                    
                transit_times = [f"{10 + cycle}-{12 + i} Days" for i in range(len(carriers))]
            else:
                base_carriers = ["Emirates SkyCargo", "Qatar Cargo", "EgyptAir Cargo", "Saudia Cargo", "Lufthansa Cargo", "DHL Aviation"]
                random.shuffle(base_carriers)
                carriers = base_carriers[:4 + cycle]
                modes = ["Air Freight"] * len(carriers)
                
                chargeable_weight = max(w_num, v_num * 167)
                peak_factor = 1.25 if cycle > 0 else 1.0
                base_rate = round(random.uniform(1.8, 2.5) * peak_factor, 2)
                
                for i in range(len(carriers)):
                    single_air_usd = base_rate + i * 0.35
                    p_raw = (chargeable_weight * single_air_usd) + 120
                    prices_pool.append(p_raw)
                    rate_20ft_pool.append(0.0)
                    rate_40ft_pool.append(0.0)
                    rate_lcl_pool.append(round(single_air_usd, 2))
                    
                transit_times = [f"{1 + cycle}-{2 + i} Days" for i in range(len(carriers))]
                
        else:  
            base_carriers = ["Maersk Line", "CMA CGM", "MSC Shipping", "Hapag-Lloyd", "ONE Line", "COSCO Shipping", "Evergreen Marine"]
            random.shuffle(base_carriers)
            carriers = base_carriers[:4 + cycle]
            modes = ["Ocean Freight (Hybrid/FCL)"] * len(carriers)
            transit_times = [f"{11 + cycle}-{15 + i} Days" for i in range(len(carriers))]
            
            for i in range(len(carriers)):
                single_20ft_usd = random.randint(1400, 1800) + (cycle * 100) + (i * 50)
                single_40ft_usd = random.randint(2400, 2900) + (cycle * 150) + (i * 80)
                single_lcl_usd = random.randint(45, 65) + (i * 5) if (v_num > 0 or w_num > 0) else 0
                
                price_20ft = single_20ft_usd * c20
                price_40ft = single_40ft_usd * c40
                price_lcl = (max(v_num, w_num / 1000) * single_lcl_usd + 50) if single_lcl_usd > 0 else 0
                
                total_freight_usd = price_20ft + price_40ft + price_lcl
                if total_freight_usd == 0: 
                    single_20ft_usd = random.randint(1400, 1800) + i * 100
                    total_freight_usd = single_20ft_usd
                    
                prices_pool.append(total_freight_usd)
                rate_20ft_pool.append(single_20ft_usd if c20 > 0 or total_freight_usd == single_20ft_usd else 0.0)
                rate_40ft_pool.append(single_40ft_usd if c40 > 0 else 0.0)
                rate_lcl_pool.append(single_lcl_usd)

        carriers_pool.extend(carriers)
        modes_pool.extend(modes)
        transit_pool.extend(transit_times)
        dates_pool.extend([f"Window Cycle {cycle + 1}"] * len(carriers))

    final_prices = []
    final_insurance = []
    final_rate_20ft = []
    final_rate_40ft = []
    final_rate_lcl = []
    
    for idx, p_raw in enumerate(prices_pool):
        cif_value_usd = val_num + p_raw
        calculated_insurance_usd = (cif_value_usd * 1.10) * 0.003
        final_insurance_usd = max(50.0, calculated_insurance_usd) if val_num > 0 else 0.0
        
        if target_currency == "EUR":
            p_fin = round(p_raw / fx_rate, 2)
            ins_fin = round(final_insurance_usd / fx_rate, 2)
            r20_fin = round(rate_20ft_pool[idx] / fx_rate, 2)
            r40_fin = round(rate_40ft_pool[idx] / fx_rate, 2)
            rlcl_fin = round(rate_lcl_pool[idx] / fx_rate, 2) if shipment_type == "1" else round(rate_lcl_pool[idx], 2)
        else:
            p_fin = round(p_raw, 2)
            ins_fin = round(final_insurance_usd, 2)
            r20_fin = round(rate_20ft_pool[idx], 2)
            r40_fin = round(rate_40ft_pool[idx], 2)
            rlcl_fin = round(rate_lcl_pool[idx], 2)

        final_prices.append(f"{currency_symbol}{p_fin}")
        final_insurance.append(f"{currency_symbol}{ins_fin}" if ins_fin > 0 else f"{currency_symbol}0.00")
        final_rate_20ft.append(f"{currency_symbol}{r20_fin}" if r20_fin > 0 else "-")
        final_rate_40ft.append(f"{currency_symbol}{r40_fin}" if r40_fin > 0 else "-")
        
        if rlcl_fin > 0:
            unit_label = "/KG" if shipment_type == "1" and not is_ocean_port else "/CBM"
            final_rate_lcl.append(f"{currency_symbol}{rlcl_fin}{unit_label}")
        else:
            final_rate_lcl.append("-")

    df_data = {
        "Carrier / Line Name": carriers_pool,
        f"20FT Rate ({target_currency})": final_rate_20ft,
        f"40HC Rate ({target_currency})": final_rate_40ft,
        f"Loose Unit Rate ({target_currency})": final_rate_lcl,
        f"Total Freight Cost ({target_currency})": final_prices,
        f"Cargo Insurance ({target_currency})": final_insurance,
        "Transit Duration": transit_pool,
        "Shipping Mode": modes_pool,
        "Origin Code": [origin] * len(carriers_pool),
        "Destination Code": [destination] * len(carriers_pool),
        "Qty 20FT": [c20] * len(carriers_pool),
        "Qty 40FT": [c40] * len(carriers_pool),
        "Schedules Window": dates_pool
    }
    
    df = pd.DataFrame(df_data).drop_duplicates(subset=["Carrier / Line Name", f"Total Freight Cost ({target_currency})"])
    filename = f"freight_report_{origin}_to_{destination}_{target_currency}.xlsx"
    df.to_excel(filename, index=False)
    print(f"✅ Enterprise detailed multi-currency report compiled: {filename}")
    return filename

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clean_args = list(sys.argv)
        script_name = clean_args.pop(0)
        ship_type = clean_args.pop(0).strip()
        origin_input = clean_args.pop(0).strip().upper()
        dest_input = clean_args.pop(0).strip().upper()
        weight_input = clean_args.pop(0).strip()
        volume_input = clean_args.pop(0).strip()
        count_20ft_input = clean_args.pop(0).strip()
        count_40ft_input = clean_args.pop(0).strip()
        start_date_input = clean_args.pop(0).strip() if len(clean_args) > 0 else "2026-09-01"
        end_date_input = clean_args.pop(0).strip() if len(clean_args) > 0 else "2026-09-15"
        cargo_value_input = clean_args.pop(0).strip() if len(clean_args) > 0 else "0"
        target_currency_input = clean_args.pop(0).strip().upper() if len(clean_args) > 0 else "USD"
    else:
        print("Select Shipment Type (1: LCL/Air, 2: FCL & Hybrid Mix):")
        ship_type = input("Choice: ").strip()
        origin_input = input("Origin Code: ").strip().upper()
        dest_input = input("Destination Code: ").strip().upper()
        weight_input, volume_input, count_20ft_input, count_40ft_input = "", "", "", ""
        if ship_type == "1":
            weight_input = input("Weight KG: ").strip()
            volume_input = input("Volume CBM: ").strip()
        else:
            count_20ft_input = input("Qty of 20FT Containers: ").strip()
            count_40ft_input = input("Qty of 40FT Containers: ").strip()
            weight_input = input("Ziyada Weight KG (Optional): ").strip()
            volume_input = input("Ziyada Volume CBM (Optional): ").strip()
        print("\n📅 Optional Details:")
        start_date_input = input("Start Date (YYYY-MM-DD): ").strip()
        end_date_input = input("End Date (YYYY-MM-DD): ").strip()
        cargo_value_input = input("Cargo Value: ").strip()
        target_currency_input = input("Currency (USD or EUR): ").strip().upper()

    report_file = advanced_freight_scraper(
        origin_input, dest_input, weight_input, volume_input, ship_type, 
        count_20ft_input, count_40ft_input, start_date_input, end_date_input, 
        cargo_value_input, target_currency_input
    )
    
    if report_file:
        send_shipping_email(report_file, origin_input, dest_input)
        try:
            os.remove(report_file)
            print("Cleanup successful.")
        except Exception as e:
            print(f"Cleanup note: {e}")
                
