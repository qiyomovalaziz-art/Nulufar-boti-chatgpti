import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


# ✅ /start bosilganda foydalanuvchi ismi bilan kutib olish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Assalomu alaykum, {user_name}! 🤖\n"
        "Nulufarxon😍 Botga xush kelibsiz!\n"
        "Savol yozing yoki rasm yuboring — men yordam beraman ✍️📸"
    )


# ✅ Matnga javob berish
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sen foydalanuvchiga yordam beradigan aqlli yordamchi botsan."},
            {"role": "user", "content": user_msg}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)


# ✅ Rasmga javob berish
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_url = file.file_path  # Telegramdan rasmi URL holida keladi

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sen rasmlarni tahlil qilib tushuntirib beradigan yordamchisan."},
            {"role": "user", "content": [
                {"type": "text", "text": "Rasimda nimalar borligini tushuntirib bering."},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)


# ✅ Asosiy ishga tushirish
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # Rasm qo‘shildi ✅

    app.run_polling()


if __name__ == "__main__":
    main()
