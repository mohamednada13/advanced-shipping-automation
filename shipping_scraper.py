import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

from air_freight import calculate_air_freight
from ocean_freight import calculate_ocean_freight

def send_shipping_email(excel_filepath, origin, destination):
    SENDER_EMAIL = "mohamednada1381979@gmail.com"  
    SENDER_PASSWORD = "ghp_umSg3WmjEgWTtKGSD1mhVZjqTpLMDm423RdM"
    RECEIVER_EMAIL = "mohamed_nada@gastec-egypt.com" 
    
    print("📨 Dispatching Final Detailed Report via Enterprise SMTP Module...")
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"📊 Freight Rates Report: {origin} ➡️ {destination}"
    
    body = f"Hi Mohamed,\n\nAttached is the automated enterprise detailed freight rates comparison report generated via dynamic multi-module architecture.\n\nRoute Details: {origin} to {destination}\n\nRegards,\nYour Advanced Cloud Automation System."
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    if excel_filepath and os.path.exists(excel_filepath):
        with open(excel_filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(excel_filepath)}")
            msg.attach(part)
            
    try:
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("🚀 Success! Rate report has been sent to your email.")
    except Exception as e:
        print(f"❌ Email transmission failed: {e}")

if __name__ == "__main__":
    v_args = []
    for arg in sys.argv:
        v_args.append(str(arg).strip())
        
    if len(v_args) > 1:
        v_args.pop(0)
        ship_type = v_args.pop(0)
        origin_input = v_args.pop(0).upper().strip()
        dest_input = v_args.pop(0).upper().strip()
        weight_input = v_args.pop(0)
        volume_input = v_args.pop(0)
        count_20ft_input = v_args.pop(0)
        count_40ft_input = v_args.pop(0)
        start_date_input = v_args.pop(0) if len(v_args) > 0 else "2026-09-01"
        end_date_input = v_args.pop(0) if len(v_args) > 0 else "2026-09-15"
        cargo_value_input = v_args.pop(0) if len(v_args) > 0 else "0"
        target_currency_input = v_args.pop(0).upper() if len(v_args) > 0 else "USD"
    else:
        ship_type = input("Choice: ").strip()
        origin_input = input("Origin: ").strip().upper()
        dest_input = input("Destination: ").strip().upper()
        weight_input = volume_input = count_20ft_input = count_40ft_input = ""
        if ship_type == "1":
            weight_input = input("Weight KG: ").strip()
            volume_input = input("Volume CBM: ").strip()
        else:
            count_20ft_input = input("Qty 20FT: ").strip()
            count_40ft_input = input("Qty 40FT: ").strip()
            weight_input = input("Total Cargo Weight KG: ").strip()
            volume_input = input("Ziyada Volume CBM: ").strip()
        start_date_input = input("Start Date: ").strip()
        end_date_input = input("End Date: ").strip()
        cargo_value_input = input("Cargo Value: ").strip()
        target_currency_input = input("Currency (USD or EUR): ").strip().upper()

    # --- 🛡️ صمام الخروج الناعم والذكي المستقل (Graceful Exit Architecture) ---
    if ship_type == "1":
        if len(origin_input) < 3 or len(origin_input) > 4 or len(dest_input) < 3 or len(dest_input) > 4:
            print("\n" + "="*60)
            print("⚠️  [INPUT VALIDATION NOTICE] AUTOMATION ENGINE IDLE")
            print("="*60)
            print(f" Your Input Location: '{origin_input}' to '{dest_input}'")
            print(" Reason: Air Freight fields require 3 or 4-character codes (IATA/ICAO).")
            print(" Action: No calculation performed. No email dispatched.")
            print(" Please check your parameters and trigger a new workflow run.")
            print("="*60 + "\n")
            sys.exit(0) # الخروج الآمن 100% باللون الأخضر دون انهيار السيرفر ميكانيكياً

    if ship_type == "2":
        if len(origin_input) != 5 or len(dest_input) != 5:
            print("\n" + "="*60)
            print("⚠️  [INPUT VALIDATION NOTICE] AUTOMATION ENGINE IDLE")
            print("="*60)
            print(f" Your Input Location: '{origin_input}' to '{dest_input}'")
            print(" Reason: Maritime Freight fields require strictly 5-character codes (UN/LOCODE).")
            print(" Action: No calculation performed. No email dispatched.")
            print(" Please check your parameters and trigger a new workflow run.")
            print("="*60 + "\n")
            sys.exit(0)

    # --- تشغيل المحرك والربط الفعلي بعد النجاح واجتياز الفحص ---
    fx_rate, currency_symbol = 1.10, "€" if target_currency_input == "EUR" else "$"
    is_ocean = (ship_type == "2")

    try:
        if is_ocean:
            final_data = calculate_ocean_freight(
                origin_input, dest_input, weight_input, volume_input, 
                count_20ft_input, count_40ft_input, ship_type, 
                cargo_value_input, target_currency_input, fx_rate, currency_symbol, start_date_input
            )
        else:
            final_data = calculate_air_freight(
                origin_input, dest_input, weight_input, volume_input, 
                cargo_value_input, target_currency_input, fx_rate, currency_symbol, start_date_input
            )

        if final_data:
            df = pd.DataFrame(final_data)
            filename = f"freight_report_{origin_input}_to_{dest_input}_{target_currency_input}.xlsx"
            df.to_excel(filename, index=False)
            send_shipping_email(filename, origin_input, dest_input)
            os.remove(filename)
            print("✨ Temporary excel artifact destroyed. Cloud server is clean!")
            
    except Exception as error:
        print(f"\n❌ [Runtime Crash] Calculation engine failed:\n{error}\n")
        sys.exit(1)
