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
    SENDER_PASSWORD = "ghp_QsE41QsLzYQBjylGg4UdfYp2u97IeB1QxS36"
    RECEIVER_EMAIL = "mohamednada1381979@gmail.com" 
    
    print("📨 Initiating Enterprise SMTP Transmission...")
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"📊 Freight Rates Report: {origin} ➡️ {destination}"
    
    body = f"Hi Mohamed,\n\nAttached is your automated detailed freight rates report.\n\nRoute: {origin} to {destination}\n\nRegards."
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    if excel_filepath and os.path.exists(excel_filepath):
        with open(excel_filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(excel_filepath)}")
            msg.attach(part)
            
    # قمنا بإزالة الـ try/except هنا لنجبر النظام على إظهار خطأ صريح إذا رفضت سيرفرات جوجل تسجيل الدخول
    server = smtplib.SMTP("://gmail.com", 587)
    server.starttls()  
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("🚀 Success! Rate report delivered to inbox.")

if __name__ == "__main__":
    v_args = [str(arg).strip() for arg in sys.argv]
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
        sys.exit("CLI interactive mode disabled on Cloud.")

    # صمام الأمان الاستباقي الصارم
    if ship_type == "1" and (len(origin_input) < 3 or len(origin_input) > 4 or len(dest_input) < 3 or len(dest_input) > 4):
        sys.exit("❌ [CRITICAL INPUT ERROR] Invalid Air Freight Selection!")
    if ship_type == "2" and (len(origin_input) != 5 or len(dest_input) != 5):
        sys.exit("❌ [CRITICAL INPUT ERROR] Invalid Ocean Freight Selection!")

    fx_rate, currency_symbol = 1.10, "€" if target_currency_input == "EUR" else "$"
    is_ocean = (ship_type == "2")

    # إزالة الـ try/except الشامل لنجعل السيرفر ينفجر بالخطأ الحقيقي أمام أعيننا لو وجد تعارض
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
        
        # 🔥 طباعة الجدول الفورية على شاشة الـ Actions لمراقبة الحسابات اللوجستية حياً
        print("\n" + "="*80)
        print(f"📊 LIVE LOGISTICS REPORT OUTPUT ({target_currency_input})")
        print("="*80)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print(df.to_string(index=False))
        print("="*80 + "\n")
        
        filename = f"freight_report_{origin_input}_to_{dest_input}_{target_currency_input}.xlsx"
        df.to_excel(filename, index=False)
        send_shipping_email(filename, origin_input, dest_input)
        os.remove(filename)
        print("✨ Environment cleanup successful.")
