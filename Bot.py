import telebot
import os
from flask import Flask
import threading

# جلب التوكن
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

# رد على أي رسالة نصية للتجربة
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == "users":
        # الرد المباشر بدون تعقيدات الآيدي مؤقتاً للتأكد من التشغيل
        bot.reply_to(message, "تم استقبال طلب القائمة، البوت يعمل!")
    else:
        bot.reply_to(message, f"وصلت رسالتك: {message.text}")

def run():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    t = threading.Thread(target=run)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
        parts = line.strip().split(" | ")
        if len(parts) >= 3:
            response += f"{i}. الايدي: {parts[0]} | الاسم: {parts[1]} | المعرف: {parts[2]}\n"
            
    response += f"\n📊 **العدد الكلي:** {len(lines)}"
    
    # حماية من تجاوز الحد الأقصى لحروف تليجرام
    if len(response) > 4000:
        with open(USERS_FILE, "rb") as doc:
            bot.send_document(ADMIN_ID, doc, caption=f"📊 العدد الكلي: {len(lines)}\n(تم إرسالها كملف لأن القائمة طويلة)")
    else:
        bot.reply_to(message, response)

# ----------------- التشغيل -----------------
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
