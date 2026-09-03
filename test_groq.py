import groq

# ===== ВСТАВЬ СВОЙ КЛЮЧ СЮДА =====
GROQ_API_KEY = "

client = groq.Client(api_key=GROQ_API_KEY)

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": "Привет! Как дела?"}],
        max_tokens=50
    )
    print("✅ Groq РАБОТАЕТ!")
    print(f"Ответ: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Groq НЕ РАБОТАЕТ: {e}")