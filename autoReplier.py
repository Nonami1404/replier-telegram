from telethon import TelegramClient, events, Button
from datetime import datetime, timedelta
import os
import sys
import asyncio

# Удаляем старую сессию, если есть
try:
    os.remove("bot.session")
except FileNotFoundError:
    pass

# Ваши данные
api_id = 25562025
api_hash = 'e7c42bb295143247bf297a54cae8bafc'
bot_token = '7420577894:AAEubMz89jYYFmtN4ppbJpT68v6AGpSy5BM'

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Храним время последнего ответа каждому юзеру
last_reply_times = {}

# Ответы на разных языках
messages = {
    "ru": "👋 Привет! Это автоответчик. Я скоро отвечу на твоё сообщение. Спасибо за ожидание!",
    "uz": "👋 Salom! Bu avtojavob. Men sizga tez orada javob beraman. Kutganingiz uchun rahmat!",
    "en": "👋 Hello! This is an auto-reply. I’ll get back to you soon. Thanks for waiting!"
}

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # ✅ Игнорируем группы и каналы
    if not event.is_private:
        return

    user_id = event.sender_id
    now = datetime.now()
    last_time = last_reply_times.get(user_id)

    if not last_time or now - last_time > timedelta(hours=1):
        await client.send_message(
            user_id,
            "👋 Выберите язык ответа:",
            buttons=[
                [Button.inline("🇷🇺 Русский", b"lang_ru")],
                [Button.inline("🇺🇿 O'zbek", b"lang_uz")],
                [Button.inline("🇬🇧 English", b"lang_en")]
            ]
        )
        last_reply_times[user_id] = now

@client.on(events.CallbackQuery)
async def callback(event):
    lang = event.data.decode().split("_")[-1]
    if lang in messages:
        await client.send_message(event.sender_id, messages[lang])
        await event.answer("Отправлено ✅", alert=False)

async def main():
    print("✅ Бот запущен")
    # Запускаем бота и ждём 1 час
    await client.start()
    await asyncio.sleep(3600)  # Ждём 1 час
    print("🔁 Перезапуск...")
    await client.disconnect()
    sys.exit(0)  # Завершаем скрипт, Railway перезапустит его

client.loop.run_until_complete(main())
