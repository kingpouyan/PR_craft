import telebot

# 🔐 توکن رباتت رو اینجا بذار
BOT_TOKEN = "8396100748:AAF-rsLmR1RBgNdZ2rWDU0nDhEmlNLK335k"

bot = telebot.TeleBot(BOT_TOKEN)

# ✅ هندلر برای شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "! ربات با موفقیت اجرا شد 🎯")

# ✅ اجرای دائم ربات
bot.infinity_polling()


