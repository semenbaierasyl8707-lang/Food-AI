from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import base64
from openai import OpenAI

# ====== ВСТАВЬ СВОИ КЛЮЧИ ======
BOT_TOKEN = "8431095703:AAFLjGfSNy7ws7RK8qcZaQtOd4F-jr0anv0"
OPENAI_API_KEY = ""
# ===============================

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT = """
Ты — профессиональный диетолог и специалист по анализу изображений еды.

Определи блюдо, ингредиенты, примерный вес порции, калорийность и БЖУ.
Ответь строго по шаблону:

🍽 Блюдо:
📦 Ингредиенты:
⚖️ Вес:
🔥 Калории:
🥩 Белки:
🧈 Жиры:
🍞 Углеводы:
📊 Уверенность:

В конце добавь:
⚠️ Все значения являются приблизительной оценкой.
"""

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = await file.download_as_bytearray()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
