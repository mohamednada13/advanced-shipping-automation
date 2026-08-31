import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_shipping_email(excel_filepath, origin, destination):
    # --- الإعدادات الثابتة والمؤمنة بالكامل ---
    SENDER_EMAIL = "mohamednada1381979@gmail.com"  
    SENDER_PASSWORD = "ghp_umSg3WmjEgWTtKGSD1mhVZjqTpLMDm423RdM"  # التوكين الآمن الخاص بك
    RECEIVER_EMAIL = "mohamednada1381979@gmail.com" 

    print("📨 [Module] Preparing final automated email report...")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"📊 Freight Rates Report: {origin} ➡️ {destination}"
    
    body = (f"Hi Mohamed,\n\n"
            f"Attached is the automated enterprise detailed freight rates comparison report.\n\n"
            f"Route Details: {origin} to {destination}\n\n"
            f"Regards,\n"
            f"Your Advanced Cloud Automation System.")
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # التحقق البرمجي الدقيق من وجود ملف الإكسيل قبل إرفاقه للحماية من الانهيار
    if excel_filepath and os.path.exists(excel_filepath):
        print(f"📎 [Module] Attaching generated excel report: {excel_filepath}")
        with open(excel_filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(excel_filepath)}")
            msg.attach(part)
    else:
        print("⚠️ [Module] Warning: Excel artifact not found. Sending text-only notification.")

    try:
        print("🔌 [Module] Establishing secure connection to Google SMTP...")
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("🚀 [Module] Success! Enterprise rate report has been delivered to your inbox.")
    except Exception as e:
        print(f"❌ [Module] Email transmission failed: {e}")
