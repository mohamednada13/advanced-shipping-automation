import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- ضع بياناتك الحقيقية هنا للتجربة ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "mohamednada1381979@gmail.com"  # إيميلك الشخصي
SENDER_PASSWORD = "mmcqpryqmbdegpfg"  # كود الـ 16 حرفاً الأصفر من جوجل
RECEIVER_EMAIL = "mohamednada1381979@gmail.com"  # نفس إيميلك الشخصي للاستقبال


def test_connection():
    print("⏳ جاري محاولة الاتصال بخادم Gmail SMTP الآمن...")

    # تنسيق رسالة نصية بسيطة جداً
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "🚀 اختبار نظام الأتمتة البريدي"

    body = "الحمد لله، إذا وصلت هذه الرسالة إلى صندوق الوارد الخاص بك، فهذا يعني أن الاتصال البريدي للسكربت سليم 100% وكود الأمان يعمل بكفاءة!"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        # بدء خط الاتصال وتشفيره
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # تشفير الاتصال لحماية البيانات

        # تسجيل الدخول عبر كود التطبيقات
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # إرسال البريد
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("\n🎉 نجاح باهر! تم إرسال إيميل الاختبار بنجاح.")
        print(
            "📥 افتح بريدك الإلكتروني الآن (صندوق الوارد أو الـ Spam) وتأكد من وصول الرسالة."
        )

    except Exception as e:
        print(f"\n❌ فشل الاتصال! حدث خطأ أثناء إرسال البريد: {e}")
        print("💡 تلميح: تأكد من مراجعة كود الـ 16 حرفاً وعدم وجود مسافات زائدة فيه.")


if __name__ == "__main__":
    test_connection()
