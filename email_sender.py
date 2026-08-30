import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_shipping_email(excel_filepath, origin, destination):
    SENDER_EMAIL = "mohamednada1381979@gmail.com"
    SENDER_PASSWORD = "mmcqpryqmbdegpfg"  # باسوورد التطبيق الخاص بك
    RECEIVER_EMAIL = "mohamednada1381979@gmail.com"

    print("📨 Preparing final automated email report...")

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = f"📊 Freight Rates Report: {origin} ➡️ {destination}"

    body = f"Hi Mohamed,\n\nAttached is the automated freight rates comparison report generated via Playwright.\n\nRoute: {origin} to {destination}\n\nRegards,\nYour Automation System."
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if excel_filepath and os.path.exists(excel_filepath):
        with open(excel_filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(excel_filepath)}",
            )
            msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("🚀 Success! Rate report has been sent to your email.")
    except Exception as e:
        print(f"❌ Email delivery failed: {e}")
