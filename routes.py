import groq
import re
import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime, timedelta


GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # ← БЕЗ ПРЯМОГО КЛЮЧА! 


client = groq.Client(api_key=GROQ_API_KEY)
router = Router()

# ===== ПАМЯТЬ =====
chat_history = {}

# ===== ЗАЩИТА ОТ СПАМА =====
user_last_message = {}

def is_spam(user_id: int, cooldown_seconds: int = 3) -> bool:
    now = datetime.now()
    if user_id in user_last_message:
        if now - user_last_message[user_id] < timedelta(seconds=cooldown_seconds):
            return True
    user_last_message[user_id] = now
    return False

async def ask_ai(user_id: int, prompt: str) -> str:
    history = chat_history.get(user_id, [])

    messages = [
        {"role": "system", "content": "Ты дружелюбный ассистент. Отвечай кратко и без лишних пояснений."}
    ] + history + [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        # ===== ФИЛЬТР ОТ РАЗМЫШЛЕНИЙ =====
        lines = answer.split('\n')
        filtered_lines = []

        for line in lines:
            if re.search(r'(analyze|think|refinement|check constraints|formulate response|user input|key requirements|final output)', line, re.IGNORECASE):
                continue
            filtered_lines.append(line)

        answer = '\n'.join(filtered_lines).strip()

        if not answer:
            sentences = re.split(r'[.!?]', ' '.join(lines))
            answer = sentences[-1].strip() if sentences else "Ответ не найден."

        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": answer})
        if len(history) > 10:
            history = history[-10:]

        chat_history[user_id] = history
        return answer

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return "Ошибка. Попробуй позже."

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я VoidX. Напиши что-нибудь.")

@router.message(Command("clear"))
async def clear_history(message: Message):
    chat_history[message.from_user.id] = []
    await message.answer("🧹 Очищено!")

@router.message()
async def handle_all_messages(message: Message):
    text = message.text
    if not text or text.startswith("/"):
        return

    user_id = message.from_user.id

    if is_spam(user_id):
        await message.answer("⏳ Не так быстро! Подожди 3 секунды.")
        return

    msg = await message.answer("Думаю...")

    answer = await ask_ai(user_id, text)

    await msg.edit_text(answer)