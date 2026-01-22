import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "topics.json")

with open(DATA_PATH, "r") as f:
    TOPICS = json.load(f)


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8388963672:AAHC_5KEuGvOhXmJN9iPVHYplJ_um2UCvEM"

app = Application.builder().token(TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Learn Topics", callback_data="learn_topics")]
    ]
    await update.message.reply_text(
        "Hey 👋\nWhat are you looking for?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Learn Topics
async def learn_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Linear Algebra", callback_data="sub_la")],
        [InlineKeyboardButton("Real Analysis", callback_data="sub_ra")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    await query.edit_message_text(
        "Which subject do you want to learn?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Linear Algebra topics
async def la_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Vector Spaces",callback_data="topic|Linear Algebra|Vector Spaces")],
        [InlineKeyboardButton("Basis & Dimension",callback_data="topic|Linear Algebra|Basis & Dimension")],

        [InlineKeyboardButton("Linear Independence", callback_data="topic_li")],
        [InlineKeyboardButton("🔙 Subjects", callback_data="learn_topics")]
    ]
    await query.edit_message_text(
        "Choose a topic from Linear Algebra 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Topic selected
async def topic_bd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("▶️ YouTube", callback_data="bd_yt")],
        [InlineKeyboardButton("📘 Books", callback_data="bd_books")],
        [InlineKeyboardButton("🧩 Practice", callback_data="bd_practice")],
        [InlineKeyboardButton("🧠 Insights", callback_data="bd_insights")],
        [InlineKeyboardButton("🔙 Topics", callback_data="sub_la")]
    ]
    await query.edit_message_text(
        "Topic: Basis & Dimension\nFollow these steps 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# YouTube content
async def show_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = context.user_data["subject"]
    topic = context.user_data["topic"]

    data = TOPICS[subject][topic]["youtube"]

    text = f"🎥 *{topic} – YouTube*\n\n"
    for x in data:
        text += f"• {x}\n"

    await query.message.reply_text(text, parse_mode="Markdown")


# Books content
async def show_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = context.user_data["subject"]
    topic = context.user_data["topic"]

    data = TOPICS[subject][topic]["books"]
    text = f"📘 *{topic} – Book References*\n\n"
    for x in data:
        text += f"• {x}\n"

    await query.message.reply_text(text, parse_mode="Markdown")



# Practice content
async def show_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = context.user_data["subject"]
    topic = context.user_data["topic"]

    data = TOPICS[subject][topic]["practice"]
    text = f"🧩 *{topic} – Practice Problems*\n\n"
    for i, q in enumerate(data, 1):
        text += f"{i}. {q}\n"

    await query.message.reply_text(text, parse_mode="Markdown")




# Insights content
async def show_insights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = context.user_data["subject"]
    topic = context.user_data["topic"]

    insight = TOPICS[subject][topic]["insights"]
    text = f"🧠 *{topic} – Key Insight*\n\n{insight}"

    await query.message.reply_text(text, parse_mode="Markdown")


async def open_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, subject, topic = query.data.split("|")

    context.user_data["subject"] = subject
    context.user_data["topic"] = topic

    keyboard = [
        [InlineKeyboardButton("▶️ YouTube", callback_data="yt")],
        [InlineKeyboardButton("📘 Books", callback_data="books")],
        [InlineKeyboardButton("🧩 Practice", callback_data="practice")],
        [InlineKeyboardButton("🧠 Insights", callback_data="insights")],
        [InlineKeyboardButton("🔙 Topics", callback_data=f"back|{subject}")]
    ]

    await query.edit_message_text(
        f"📘 Topic: *{topic}*\n\nFollow these steps 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )




# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(learn_topics, pattern="learn_topics"))
app.add_handler(CallbackQueryHandler(la_topics, pattern="sub_la"))
app.add_handler(CallbackQueryHandler(topic_bd, pattern="topic_bd"))

app.add_handler(CallbackQueryHandler(show_books, pattern="books"))
app.add_handler(CallbackQueryHandler(show_practice, pattern="practice"))
app.add_handler(CallbackQueryHandler(show_insights, pattern="insights"))

app.add_handler(CallbackQueryHandler(open_topic, pattern="^topic\\|"))
app.add_handler(CallbackQueryHandler(show_youtube, pattern="yt"))

app.run_polling()
import time
while true:
    time.sleep(1000)