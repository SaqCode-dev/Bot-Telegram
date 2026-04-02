import telebot
from telebot import types # استيراد أنواع الأزرار
from flask import Flask
import threading
import os

# جلب التوكن من متغيرات البيئة لضمان الأمان
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت يعمل بنجاح 24/7!"

def run_bot():
    bot.infinity_polling()

# تعديل أمر start لإضافة الزر الشفاف
@bot.message_handler(commands=['start'])
def send_welcome_command(message):
    # إنشاء لوحة المفاتيح الشفافة
    markup = types.InlineKeyboardMarkup()
    
    # إنشاء الزر مع الرابط
    developer_button = types.InlineKeyboardButton(
        text="📱 تواصل مع المطور", 
        url="https://t.me/SaqCode"
    )
    
    # إضافة الزر للوحة
    markup.add(developer_button)
    
    # إرسال الرسالة مع الزر
    bot.reply_to(
        message, 
        "مرحبا بك في بوت مكتبه شغف.\nهذا البوت إدارة الموقع وليس للمستخدمين", 
        reply_markup=markup
    )

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
