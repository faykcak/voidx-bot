import os
import threading
from flask import Flask
from main import main, bot, dp  # Импортируем бота из твоего файла

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    """Запускает основную функцию бота в отдельном потоке."""
    import asyncio
    asyncio.run(main())

if __name__ == "__main__":
    # Запускаем бота в фоновом потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Запускаем Flask-сервер, чтобы Render не ругался
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)