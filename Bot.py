import telebot
import os
import threading
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# =================== الإعدادات ===================
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# =================== محتوى البوت (عدّل هنا) ===================
INFO = {
    "name": "اسمك الكامل",
    "title": "مطور | مصمم | ...",
    "about": (
        "👋 مرحباً! أنا [اسمك].\n\n"
        "أعمل في مجال تطوير البرمجيات منذ X سنوات.\n"
        "شغوف بالتكنولوجيا وبناء حلول مبتكرة."
    ),
    "skills": (
        "🛠 *مهاراتي التقنية:*\n\n"
        "• Python / Django\n"
        "• JavaScript / React\n"
        "• قواعد البيانات: MySQL, MongoDB\n"
        "• DevOps: Docker, Git\n"
        "• تصميم UI/UX"
    ),
    "projects": (
        "💻 *مشاريعي:*\n\n"
        "1️⃣ *مشروع أول*\n"
        "   وصف مختصر للمشروع\n"
        "   🔗 [رابط المشروع](https://example.com)\n\n"
        "2️⃣ *مشروع ثانٍ*\n"
        "   وصف مختصر للمشروع\n"
        "   🔗 [رابط المشروع](https://example.com)\n\n"
        "3️⃣ *مشروع ثالث*\n"
        "   وصف مختصر للمشروع\n"
        "   🔗 [رابط المشروع](https://example.com)"
    ),
    "contact": (
        "📬 *تواصل معي:*\n\n"
        "📧 البريد: example@email.com\n"
        "💼 LinkedIn: [اسمك](https://linkedin.com)\n"
        "🐙 GitHub: [اسمك](https://github.com)\n"
        "🐦 Twitter: @اسمك"
    ),
    "website": "https://yourwebsite.com",
    "cv_url": "https://link-to-your-cv.com",
    "welcome": (
        "👋 مرحباً بك!\n\n"
        "هذا البوت هو بوابتي الشخصية.\n"
        "اختر ما تريد من القائمة أدناه أو استخدم الأوامر المباشرة:"
    )
}

# =================== Flask ===================
@app.route('/')
def home():
    return "Bot is Alive!"

# =================== لوحة الأزرار الرئيسية ===================
def main_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💻 مشاريعي", callback_data="projects"),
        InlineKeyboardButton("👤 حول", callback_data="about"),
        InlineKeyboardButton("⚙️ مهاراتي", callback_data="skills"),
        InlineKeyboardButton("📞 تواصل معي", callback_data="contact"),
        InlineKeyboardButton("📄 سيرتي الذاتية", callback_data="cv"),
        InlineKeyboardButton("🌐 موقعي", callback_data="website"),
    )
    return markup

def back_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
    return markup

# =================== تسجيل الأوامر في تيليجرام ===================
def set_bot_commands():
    commands = [
        BotCommand("start",    "ابدأ من هنا"),
        BotCommand("menu",     "القائمة الرئيسية"),
        BotCommand("about",    "من أنا"),
        BotCommand("skills",   "مهاراتي"),
        BotCommand("projects", "مشاريعي"),
        BotCommand("contact",  "تواصل معي"),
        BotCommand("cv",       "سيرتي الذاتية"),
        BotCommand("website",  "موقعي الإلكتروني"),
    ]
    bot.set_my_commands(commands)

# =================== أوامر البوت ===================
@bot.message_handler(commands=["start", "menu"])
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        INFO["welcome"],
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=["about"])
def cmd_about(message):
    bot.send_message(message.chat.id, INFO["about"], reply_markup=back_keyboard())

@bot.message_handler(commands=["skills"])
def cmd_skills(message):
    bot.send_message(
        message.chat.id, INFO["skills"],
        parse_mode="Markdown", reply_markup=back_keyboard()
    )

@bot.message_handler(commands=["projects"])
def cmd_projects(message):
    bot.send_message(
        message.chat.id, INFO["projects"],
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=back_keyboard()
    )

@bot.message_handler(commands=["contact"])
def cmd_contact(message):
    bot.send_message(
        message.chat.id, INFO["contact"],
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=back_keyboard()
    )

@bot.message_handler(commands=["cv"])
def cmd_cv(message):
    bot.send_message(
        message.chat.id,
        f"📄 *سيرتي الذاتية:*\n\n🔗 [اضغط هنا لتحميل السيرة الذاتية]({INFO['cv_url']})",
        parse_mode="Markdown",
        reply_markup=back_keyboard()
    )

@bot.message_handler(commands=["website"])
def cmd_website(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🌐 زيارة الموقع", url=INFO["website"]))
    markup.add(InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
    bot.send_message(
        message.chat.id,
        f"🌐 *موقعي الإلكتروني:*\n\n{INFO['website']}",
        parse_mode="Markdown",
        reply_markup=markup
    )

# =================== معالجة أزرار Inline ===================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    msg_id  = call.message.message_id

    if call.data == "main_menu":
        bot.edit_message_text(
            INFO["welcome"],
            chat_id, msg_id,
            reply_markup=main_keyboard()
        )

    elif call.data == "about":
        bot.edit_message_text(
            INFO["about"],
            chat_id, msg_id,
            reply_markup=back_keyboard()
        )

    elif call.data == "skills":
        bot.edit_message_text(
            INFO["skills"],
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif call.data == "projects":
        bot.edit_message_text(
            INFO["projects"],
            chat_id, msg_id,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=back_keyboard()
        )

    elif call.data == "contact":
        bot.edit_message_text(
            INFO["contact"],
            chat_id, msg_id,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=back_keyboard()
        )

    elif call.data == "cv":
        bot.edit_message_text(
            f"📄 *سيرتي الذاتية:*\n\n🔗 [اضغط هنا لتحميل السيرة الذاتية]({INFO['cv_url']})",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif call.data == "website":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🌐 زيارة الموقع", url=INFO["website"]))
        markup.add(InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(
            f"🌐 *موقعي الإلكتروني:*\n\n{INFO['website']}",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

    bot.answer_callback_query(call.id)

# =================== أي رسالة أخرى ===================
@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.send_message(
        message.chat.id,
        "استخدم /menu لعرض القائمة الرئيسية 👇",
        reply_markup=main_keyboard()
    )

# =================== التشغيل ===================
def run_bot():
    set_bot_commands()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
