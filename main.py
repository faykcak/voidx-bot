import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.routes import router

load_dotenv()

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===== ПРЯМАЯ ПЕРЕДАЧА КЛЮЧА В ОКРУЖЕНИЕ =====
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

print(f"🔍 TOKEN: {TOKEN[:10]}...")
print(f"🔍 GROQ_API_KEY: {GROQ_API_KEY[:15]}...")




if not TOKEN:
    raise ValueError("❌ TOKEN не найден в .env")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY не найден в .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())