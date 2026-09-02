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
    RECEIVER_EMAIL = "mohamednada1381979@gmail.com" 
    
    # 🎯 تم التصحيح الصارم والنهائي لعنوان سيرفر جوجل والبورت هنا
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 465
    
    # 🔐 قراءة كلمة سر التطبيق الصافية والجديدية من الخزنة السحابية لجيت هاب بأمان
    SENDER_PASSWORD = os.environ.get("GMAIL_PASSWORD_TOKEN")
    if not SENDER_PASSWORD:
        print("⚠️ Warning: GMAIL_PASSWORD_TOKEN environment variable is missing on cloud runner.")
        return

    print(f"📨 Opening Secure SSL SMTP Connection to {SMTP_SERVER} on Port {SMTP_PORT}...")
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"📊 Freight Rates Report: {origin} ➡️ {destination}"
    
    body = f"Hi Mohamed,\n\nAttached is your automated enterprise detailed freight rates report generated via dynamic multi-module architecture.\n\nRoute Details: {origin} to {destination}\n\nRegards."
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    if excel_filepath and os.path.exists(excel_filepath):
        with open(excel_filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(excel_filepath)}")
            msg.attach(part)
            
    try:
        # الاتصال المباشر والآمن بقناة جوجل المشفرة بالكامل
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("🚀 Success! Rate report has been sent to your email.")
    except Exception as e:
        print(f"❌ Email transmission layer error: {e}")

if __name__ == "__main__":
    ship_type = "1"
    origin_input = "CAI"
    dest_input = "LHR"
    weight_input = "100"
    volume_input = "1"
    count_20ft_input = "0"
    count_40ft_input = "0"
    start_date_input = "2026-09-01"
    end_date_input = "2026-09-15"
    cargo_value_input = "0"
    target_currency_input = "EUR"

    if len(sys.argv) > 1: ship_type = str(sys.argv).strip()
    if len(sys.argv) > 2: origin_input = str(sys.argv).upper().strip()
    if len(sys.argv) > 3: dest_input = str(sys.argv).upper().strip()
    if len(sys.argv) > 4: weight_input = str(sys.argv).strip()
    if len(sys.argv) > 5: volume_input = str(sys.argv).strip()
    if len(sys.argv) > 6: count_20ft_input = str(sys.argv).strip()
    if len(sys.argv) > 7: count_40ft_input = str(sys.argv).strip()
    if len(sys.argv) > 8: start_date_input = str(sys.argv).strip()
    if len(sys.argv) > 9: end_date_input = str(sys.argv).strip()
    if len(sys.argv) > 10: cargo_value_input = str(sys.argv).strip()
    if len(sys.argv) > 11: target_currency_input = str(sys.argv).upper().strip()

    is_ocean = (len(origin_input) == 5 or len(dest_input) == 5)

    if not is_ocean:
        if len(origin_input) < 3 or len(origin_input) > 4 or len(dest_input) < 3 or len(dest_input) > 4:
            print("\n" + "="*70 + "\n⚠️  [INPUT VALIDATION NOTICE] AUTOMATION ENGINE IDLE\n" + "="*70)
            sys.exit(0)
    else:
        if len(origin_input) != 5 or len(dest_input) != 5:
            print("\n" + "="*70 + "\n⚠️  [INPUT VALIDATION NOTICE] AUTOMATION ENGINE IDLE\n" + "="*70)
            sys.exit(0)

    fx_rate, currency_symbol = 1.10, "€" if target_currency_input == "EUR" else "$"

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
            print("\n" + "="*80)
            print(df.to_string(index=False))
            print("="*80 + "\n")
            
            filename = f"freight_report_{origin_input}_to_{dest_input}_{target_currency_input}.xlsx"
            df.to_excel(filename, index=False)
            send_shipping_email(filename, origin_input, dest_input)
            os.remove(filename)
            print("✨ Cleanup successful.")
            
    except Exception as error:
        print(f"\n❌ Calculation failed:\n{error}\n")
        sys.exit(1)
