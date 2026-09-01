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
    
    # 🔐 Securely extraction of your clean 16-character app password from the vault environment
    SENDER_PASSWORD = os.environ.get("GMAIL_PASSWORD_TOKEN")
    if not SENDER_PASSWORD:
        print("⚠️ Warning: GMAIL_PASSWORD_TOKEN environment variable is missing on cloud runner.")
        return

    print("📨 Opening Clean SMTP Connection to Google Servers...")
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
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("🚀 Success! Rate report has been sent to your email.")
    except Exception as e:
        print(f"❌ Email transmission layer error: {e}")

if __name__ == "__main__":
    v_args = []
    for arg in sys.argv:
        v_args.append(str(arg).strip())
        
    if len(v_args) > 1:
        v_args.pop(0) # Remove script name entry
        ship_type = v_args
        origin_input = v_args.upper().strip()
        dest_input = v_args.upper().strip()
        weight_input = v_args
        volume_input = v_args
        count_20ft_input = v_args
        count_40ft_input = v_args
        start_date_input = v_args if len(v_args) > 7 else "2026-09-01"
        end_date_input = v_args if len(v_args) > 8 else "2026-09-15"
        cargo_value_input = v_args if len(v_args) > 9 else "0"
        target_currency_input = v_args.upper() if len(v_args) > 10 else "USD"
    else:
        sys.exit("CLI interactive mode disabled on Cloud Run environment.")

    # --- 🛡️ Graceful Exit Pre-Validation Guardrails ---
    if ship_type == "1":
        if len(origin_input) < 3 or len(origin_input) > 4 or len(dest_input) < 3 or len(dest_input) > 4:
            print("\n" + "="*70 + "\n⚠️  [INPUT VALIDATION NOTICE] AUTOMATION ENGINE IDLE\n" + "="*70)
            print(" Reason: Air Freight fields require strictly 3 or 4-character codes (IATA/ICAO).")
            print(" Action: No calculation performed. No email transmission triggered.\n" + "="*70 + "\n")
            sys.exit(0)

    if ship_type == "2":
        if len(origin_input) != 5 or len(dest_input) != 5:
            print("\n" + "="*70 + "\n⚠️  [INPUT VALIDATION NOTICE] AUTOMATION ENGINE IDLE\n" + "="*70)
            print(" Reason: Ocean Freight fields require strictly 5-character codes (UN/LOCODE).")
            print(" Action: No calculation performed. No email transmission triggered.\n" + "="*70 + "\n")
            sys.exit(0)

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
            
    except Exception as error:
        print(f"\n❌ [Runtime Crash] Calculation engine failed:\n{error}\n")
        sys.exit(1)
