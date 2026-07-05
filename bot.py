import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# =========================
# 🔐 CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing in environment variables!")

# =========================
# 📊 LOGGING (Railway safe)
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# =========================
# 📚 BOOK SEARCH FUNCTION
# =========================

def search_books(query: str):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        response = requests.get(url, timeout=10)
        data = response.json()

        items = data.get("items", [])

        if not items:
            return "❌ هېڅ کتاب پیدا نه شو\n👉 بل نوم try کړه"

        result = ""

        for item in items:
            info = item.get("volumeInfo", {})

            title = info.get("title", "No Title")
            authors = ", ".join(info.get("authors", ["Unknown"]))
            link = info.get("infoLink", "")

            result += f"📚 {title}\n👤 {authors}\n🔗 {link}\n\n"

        return result[:3500]

    except Exception as e:
        logger.error(f"Search error: {e}")
        return "⚠️ API یا Network مشکل"

# =========================
# 🧠 SMART ROUTER
# =========================

def smart(text: str):
    text = text.lower()

    if "python" in text or "پایتون" in text:
        return search_books("python programming")

    if "math" in text or "ریاضی" in text:
        return search_books("mathematics")

    if "islam" in text or "اسلام" in text:
        return search_books("islamic books")

    return search_books(text)

# =========================
# 🤖 HANDLERS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n📚 کتاب نوم ولیکه زه به درته پیدا کړم"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        result = smart(text)
        await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"Handler error: {e}")
        await update.message.reply_text("⚠️ Error occurred")

# =========================
# 🚀 MAIN APP
# =========================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    logger.info("🤖 Bot is running...")
    app.run_polling(
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()def smart(text):
    text = text.lower()

    if "python" in text or "پایتون" in text:
        return search_books("python programming")

    if "math" in text or "ریاضی" in text:
        return search_books("mathematics")

    if "islam" in text or "اسلام" in text:
        return search_books("islamic books")

    return search_books(text)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n📚 کتاب نوم ولیکه زه به درته پیدا کړم"
    )

# message handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        result = smart(text)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text("⚠️ Error occurred")

# main
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🤖 Bot running...")
app.run_polling()
