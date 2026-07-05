import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ✅ SAFE TOKEN (Railway variable)
TOKEN = os.getenv("BOT_TOKEN")

# 📚 Search function
def search_books(query):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        r = requests.get(url, timeout=10).json()

        items = r.get("items", [])

        if not items:
            return "❌ هېڅ کتاب پیدا نه شو\n👉 بل نوم ولیکه"

        result = ""

        for item in items:
            info = item.get("volumeInfo", {})

            title = info.get("title", "No Title")
            authors = ", ".join(info.get("authors", ["Unknown"]))
            link = info.get("infoLink", "")

            result += f"📚 {title}\n👤 {authors}\n🔗 {link}\n\n"

        return result[:3500]  # safe limit

    except:
        return "⚠️ Network error یا API مشکل"

# 🧠 smart routing
def smart(text):
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
