import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8593578684:AAFOyFgjmO4RogWyZkO8sV_PPL9ala6oW20"  # 🔴 خپل token دلته واچوه

# 📚 Book Search (Google Books API)
def search_books(query):
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        r = requests.get(url, timeout=10).json()

        items = r.get("items", [])

        if not items:
            return "❌ هېڅ کتاب پیدا نه شو\n👉 بل نوم try کړه"

        result = ""

        for item in items:
            info = item.get("volumeInfo", {})

            title = info.get("title", "No Title")
            authors = ", ".join(info.get("authors", ["Unknown"]))
            link = info.get("infoLink", "")

            result += f"📚 {title}\n👤 {authors}\n🔗 {link}\n\n"

        return result

    except:
        return "⚠️ Network یا API error"

# 🧠 SMART SEARCH
def smart(text):
    text = text.lower()

    if "python" in text or "پایتون" in text:
        return search_books("python programming")

    if "math" in text or "ریاضی" in text:
        return search_books("mathematics")

    if "islam" in text or "اسلام" in text:
        return search_books("islamic books")

    return search_books(text)

# 🤖 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n📚 کتاب نوم ولیکه زه به درته پیدا کړم"
    )

# 🔍 MESSAGE HANDLER
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = smart(text)
    await update.message.reply_text(result)

# 🚀 RUN BOT
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🤖 Clean Bot Running...")
app.run_polling()
