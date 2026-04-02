import telebot
from telebot import types
from flask import Flask
import threading
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# آيدي الإدارة الخاص بك (تأكد من أنه نفس الحساب الذي تراسل منه)
ADMIN_ID = 8500943747
USERS_FILE = "users_info.txt"

def save_user_info(user):
    users_ids = set()
    count = 0
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    count += 1
                    uid = line.split(" | ")[0]
                    users_ids.add(uid)
    
    is_new = str(user.id) not in users_ids
    if is_new:
        name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        username = f"@{user.username}" if user.username else "لا يوجد"
        with open(USERS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{user.id} | {name} | {username}\n")
        count += 1
    return is_new, count

@app.route('/')
def home():
    return "البوت يعمل بنجاح 24/7!"

def run_bot():
    bot.infinity_polling()

@bot.message_handler(commands=['start'])
def send_welcome_command(message):
    user = message.from_user
    is_new, total_count = save_user_info(user)
    
    if is_new:
        name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        username = f"@{user.username}" if user.username else "لا يوجد"
        admin_text = (
            f"تم دخول شخص جديد 👾\n"
            f"الاسم : {name}\n"
            f"معرف : {username}\n"
            f"الايدي : {user.id}\n"
            f"عدد الأعضاء : {total_count}"
        )
        try: bot.send_message(ADMIN_ID, admin_text)
        except: pass

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="📱 تواصل مع المطور", url="https://t.me/SaqCode"))
    bot.reply_to(message, "مرحبا بك في بوت مكتبه شغف.\nهذا البوت إدارة الموقع وليس للمستخدمين", reply_markup=markup)

# تعديل شرط أمر users ليكون أكثر مرونة
@bot.message_handler(func=lambda message: message.text and message.text.strip().lower() == "users")
def show_all_users(message):
    # طباعة الآيدي في الـ Logs للتأكد (اختياري للمطور)
    print(f"Message from: {message.from_user.id}") 
    
    if int(message.from_user.id) != ADMIN_ID:
        bot.reply_to(message, "عذراً، هذا الأمر مخصص للإدارة فقط 🚫")
        return
        
    if not os.path.exists(USERS_FILE):
        bot.reply_to(message, "لا يوجد مستخدمين مسجلين حتى الآن.")
        return
        
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    if not lines:
        bot.reply_to(message, "القائمة فارغة.")
        return
        
    response = "👥 **قائمة المستخدمين:**\n\n"
    for i, line in enumerate(lines, 1):
        response += f"{i}. {line.strip()}\n"
    response += f"\n📊 **العدد الكلي:** {len(lines)}"
    
    if len(response) > 4000:
        with open(USERS_FILE, "rb") as doc:
            bot.send_document(ADMIN_ID, doc, caption=f"📊 العدد: {len(lines)}")
    else:
        bot.reply_to(message, response)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
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
