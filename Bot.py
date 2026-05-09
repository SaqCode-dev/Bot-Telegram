import telebot
import os
import threading
from flask import Flask

# =================== الإعدادات ===================
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
USERS_FILE = "users.txt"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# =================== Flask ===================
@app.route('/')
def home():
    return "Bot is Alive!"

# =================== حفظ المستخدمين ===================
def save_user(user):
    user_id = str(user.id)
    username = user.username or "بدون معرف"
    full_name = (user.first_name or "") + " " + (user.last_name or "")
    full_name = full_name.strip() or "بدون اسم"

    # تحقق من التكرار
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(user_id + " | "):
                    return  # المستخدم موجود مسبقاً

    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user_id} | {full_name} | @{username}\n")

# =================== معالجة الرسائل ===================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    save_user(message.from_user)

    if message.text.lower() == "users":
        # فقط الأدمن يمكنه رؤية القائمة
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "⛔ ليس لديك صلاحية.")
            return

        if not os.path.exists(USERS_FILE):
            bot.reply_to(message, "📭 لا يوجد مستخدمون بعد.")
            return

        with open(USERS_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]

        if not lines:
            bot.reply_to(message, "📭 القائمة فارغة.")
            return

        response = "📋 **قائمة المستخدمين:**\n\n"
        for i, line in enumerate(lines, 1):
            parts = line.split(" | ")
            if len(parts) >= 3:
                response += f"{i}. الايدي: {parts[0]} | الاسم: {parts[1]} | المعرف: {parts[2]}\n"

        response += f"\n📊 **العدد الكلي:** {len(lines)}"

        if len(response) > 4000:
            with open(USERS_FILE, "rb") as doc:
                bot.send_document(
                    ADMIN_ID, doc,
                    caption=f"📊 العدد الكلي: {len(lines)}\n(تم إرسالها كملف لأن القائمة طويلة)"
                )
        else:
            bot.reply_to(message, response)
    else:
        bot.reply_to(message, f"وصلت رسالتك: {message.text}")

# =================== التشغيل ===================
def run_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
