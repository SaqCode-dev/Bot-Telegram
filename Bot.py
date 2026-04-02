import telebot
from telebot import types
from flask import Flask
import threading
import os

# جلب التوكن من منصة Render
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ضع الآيدي (ID) الخاص بك هنا لكي تصلك الإشعارات (تأكد من الرقم)
ADMIN_ID = 8500943747

# اسم الملف الذي سنحفظ فيه آيديهات الأعضاء لعدهم
USERS_FILE = "users.txt"

# دالة لحفظ العضو الجديد وحساب العدد الإجمالي
def add_user_and_get_count(user_id):
    users = set()
    # قراءة الأعضاء السابقين إذا كان الملف موجوداً
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                users.add(line.strip())
    
    # هل المستخدم جديد؟
    is_new = str(user_id) not in users
    if is_new:
        users.add(str(user_id))
        # إضافة العضو الجديد للملف
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")
            
    return is_new, len(users)

@app.route('/')
def home():
    return "البوت يعمل بنجاح 24/7!"

def run_bot():
    bot.infinity_polling()

@bot.message_handler(commands=['start'])
def send_welcome_command(message):
    user = message.from_user
    
    # 1. فحص وتسجيل العضو
    is_new, total_count = add_user_and_get_count(user.id)
    
    # 2. إذا كان الشخص جديداً، أرسل إشعاراً للأدمن
    if is_new:
        # ترتيب الاسم
        name = user.first_name
        if user.last_name:
            name += f" {user.last_name}"
            
        # ترتيب المعرف
        username = f"@{user.username}" if user.username else "لا يوجد"
        
        # رسالة الأدمن (مطابقة لطلبك)
        admin_text = (
            f"تم دخول شخص جديد إلى البوت الخاص بك 👾\n\n"
            f"-----------------------\n"
            f"• معلومات العضو الجديد .\n\n"
            f"• الاسم : {name}\n"
            f"• معرف : {username}\n"
            f"• الايدي : {user.id}\n"
            f"-----------------------\n"
            f"• عدد الأعضاء الكلي : {total_count}"
        )
        
        try:
            bot.send_message(ADMIN_ID, admin_text)
        except Exception as e:
            print(f"لم أتمكن من إرسال رسالة للأدمن، تأكد من الآيدي: {e}")

    # 3. إرسال رسالة الترحيب للمستخدم العادي (مع الزر الشفاف)
    markup = types.InlineKeyboardMarkup()
    developer_button = types.InlineKeyboardButton(
        text="📱 تواصل مع المطور", 
        url="https://t.me/SaqCode"
    )
    markup.add(developer_button)
    
    bot.reply_to(
        message, 
        "مرحبا بك في بوت مكتبه شغف.\nهذا البوت إدارة الموقع وليس للمستخدمين", 
        reply_markup=markup
    )

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
