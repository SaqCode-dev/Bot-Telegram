import telebot
from telebot import types
from flask import Flask
import threading
import os

# التوكن
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# آيدي الإدارة الخاص بك
ADMIN_ID = 8500943747

# ملف جديد لحفظ البيانات كاملة
USERS_FILE = "users_info.txt"

# دالة لحفظ بيانات العضو كاملة (الآيدي، الاسم، المعرف)
def save_user_info(user):
    users_ids = set()
    count = 0
    
    # قراءة الملف لمعرفة الأعضاء السابقين وعددهم
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    count += 1
                    try:
                        # استخراج الآيدي من السطر لفحصه
                        uid = line.split(" | ")[0]
                        users_ids.add(uid)
                    except:
                        pass
                        
    # هل المستخدم جديد؟
    is_new = str(user.id) not in users_ids
    if is_new:
        # تجهيز الاسم
        name = user.first_name
        if user.last_name:
            name += f" {user.last_name}"
            
        # تجهيز المعرف
        username = f"@{user.username}" if user.username else "لا يوجد"
        
        # حفظ البيانات في الملف الجديد
        with open(USERS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{user.id} | {name} | {username}\n")
        count += 1
        
    return is_new, count

# ----------------- سيرفر الويب -----------------
@app.route('/')
def home():
    return "البوت يعمل بنجاح 24/7!"

def run_bot():
    bot.infinity_polling()

# ----------------- أوامر البوت -----------------

# 1. أمر الاستارت
@bot.message_handler(commands=['start'])
def send_welcome_command(message):
    user = message.from_user
    
    # حفظ العضو وجلب العدد
    is_new, total_count = save_user_info(user)
    
    # إرسال إشعار للأدمن إذا كان جديداً
    if is_new:
        name = user.first_name
        if user.last_name: name += f" {user.last_name}"
        username = f"@{user.username}" if user.username else "لا يوجد"
        
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
        except:
            pass

    # رسالة المستخدم العادي والزر
    markup = types.InlineKeyboardMarkup()
    developer_button = types.InlineKeyboardButton(text="📱 تواصل مع المطور", url="https://t.me/SaqCode")
    markup.add(developer_button)
    
    bot.reply_to(message, "مرحبا بك في بوت مكتبه شغف.\nهذا البوت إدارة الموقع وليس للمستخدمين", reply_markup=markup)


# 2. أمر الإدارة (استخراج الأعضاء)
@bot.message_handler(func=lambda message: message.text.lower() == "users")
def show_all_users(message):
    # التحقق من أن المرسل هو أنت فقط!
    if str(message.from_user.id) != str(ADMIN_ID):
        bot.reply_to(message, "عذراً، هذا الأمر مخصص للإدارة فقط 🚫")
        return
        
    # التأكد من وجود أعضاء
    if not os.path.exists(USERS_FILE):
        bot.reply_to(message, "لا يوجد مستخدمين حتى الآن.")
        return
        
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    if not lines:
        bot.reply_to(message, "لا يوجد مستخدمين حتى الآن.")
        return
        
    # تنسيق الرسالة
    response = "👥 **قائمة المستخدمين:**\n\n"
    for i, line in enumerate(lines, 1):
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
