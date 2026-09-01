import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

# استدعاء المحركات الجوية والبحرية المنفصلة تلبية للشروط الهندسية واللوجستية الاحترافية
from air_freight import calculate_air_freight
from ocean_freight import calculate_ocean_freight

def send_shipping_email(excel_filepath, origin, destination):
    SENDER_EMAIL = "mohamednada1381979@gmail.com"  
    SENDER_PASSWORD = "ghp_umSg3WmjEgWTtKGSD1mhVZjqTpLMDm423RdM"
    RECEIVER_EMAIL = "mohamednada1381979@gmail.com" 
    
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
        origin_input = v_args.pop(0).upper()
        dest_input = v_args.pop(0).upper()
        weight_input = v_args.pop(0)
        volume_input = v_args.pop(0)
        count_20ft_input = v_args.pop(0)
        count_40ft_input = v_args.pop(0)
        start_date_input = v_args.pop(0) if len(v_args) > 0 else "2026-09-01"
        end_date_input = v_args.pop(0) if len(v_args) > 0 else "2026-09-15"
        cargo_value_input = v_args.pop(0) if len(v_args) > 0 else "0"
        target_currency_input = v_args.pop(0).upper() if len(v_args) > 0 else "USD"
    else:
        print("Select Shipment Type (1: LCL/Air, 2: FCL & Hybrid Mix):")
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

    fx_rate, currency_symbol = 1.10, "€" if target_currency_input == "EUR" else "$"
    
    # التوجيه الذكي الصارم بناءً على فحص طول الأكواد الجغرافية للفصل التام
    is_ocean = len(origin_input) == 5 or len(dest_input) == 5
    
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
            
            # استدعاء دالة الإرسال الآمن عبر البريد الإلكتروني
            send_shipping_email(filename, origin_input, dest_input)
            
            # تدمير ملف الإكسيل المؤقت لمنع التراكم على خوادم السحاب
            os.remove(filename)
            print("✨ Temporary excel artifact destroyed. Cloud server is clean!")
            
    except Exception as error:
        print(f"\n❌ [Validation Triggered] System stopped execution: {error}\n")
        sys.exit(1)
