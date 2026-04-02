import telebot
from flask import Flask
import threading
import os

# الصق التوكن الخاص بك هنا
# بدلاً من وضع التوكن هنا، سنطلبه من النظام
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# صفحة ويب بسيطة للتأكد من أن السيرفر يعمل وسنستخدمها لإبقاء البوت مستيقظاً
@app.route('/')
def home():
    return "البوت يعمل بنجاح 24/7!"

# دالة لتشغيل البوت
def run_bot():
    bot.infinity_polling()

# الرد على أوامر تليجرام
@bot.message_handler(commands=['start'])
def send_welcome_command(message):
    bot.reply_to(message, "مرحبا بك في بوت مكتبه شغف.\n هذا البوت إدارة الموقع وليس للمستخدمين")

if __name__ == "__main__":
    # تشغيل البوت في مسار (Thread) منفصل حتى لا يوقف سيرفر الويب
    threading.Thread(target=run_bot).start()
    
    # تشغيل سيرفر الويب (المنفذ ضروري لتعمل الاستضافة)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
