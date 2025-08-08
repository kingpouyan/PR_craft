import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# تنظیمات اولیه

BOT_TOKEN = "8396100748:AAF-rsLmR1RBgNdZ2rWDU0nDhEmlNLK335"
USERNAME = "POUYAN001"
PASSWORD = "pooyan1391"
SERVER_NAME = "POUYAN001"  # دقیقاً همونی که تو داشبورد می‌بینی

# =========================
# ورود به Aternos و دریافت کوکی نشست

def get_session():
    session = requests.Session()
    login_url = "https://aternos.org/go/"
    session.get(login_url)

    payload = {
        'user': USERNAME,
        'password': PASSWORD
    }
    r = session.post("https://aternos.org/panel/ajax/account/login.php", data=payload)

    if "login" in r.text:
        return session
    else:
        return None

# =========================
# بررسی وضعیت سرور

def get_server_status(session):
    response = session.get("https://aternos.org/panel/ajax/status.php")
    data = response.json()
    return data

# =========================
# روشن کردن سرور

def start_server(session):
    response = session.get("https://aternos.org/panel/ajax/start.php")
    return response.text

# =========================
# دستورات ربات

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋\nدستور /status رو بزن تا وضعیت سرور Aternos رو ببینی.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال بررسی وضعیت سرور...")

    session = get_session()
    if not session:
        await update.message.reply_text("❌ ورود به Aternos با خطا مواجه شد.")
        return

    data = get_server_status(session)
    status = data.get("status")

    if status == "offline":
        await update.message.reply_text("سرور خاموشه. در حال روشن کردن...")
        result = start_server(session)
        if "request" in result:
            await update.message.reply_text("✅ درخواست روشن شدن سرور ارسال شد.")
        else:
            await update.message.reply_text("❌ نتونستم سرور رو روشن کنم.")
    elif status == "online":
        await update.message.reply_text("✅ سرور الان آنلاینه.")
    elif status == "starting":
        await update.message.reply_text("⏳ سرور در حال روشن شدنه.")
    else:
        await update.message.reply_text(f"❓ وضعیت سرور نامشخصه: {status}")

# =========================
# راه‌اندازی ربات

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    print("ربات آماده اجراست...")
    app.run_polling()

