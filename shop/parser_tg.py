import os  # работа с переменными окружения (.env)
import re  # (может пригодиться для обработки текста)
from telethon import TelegramClient  # клиент для Telegram API
from dotenv import load_dotenv  # загрузка .env файла
from asgiref.sync import sync_to_async  # обёртка для Django ORM в async
from django.utils.text import slugify  # генерация slug

from shop.models import Blog  # модель блога

# ------------------------------
# 🔐 ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# ------------------------------
load_dotenv()

api_id = int(os.getenv("API_ID"))  # Telegram API ID
api_hash = os.getenv("API_HASH")  # Telegram API HASH
channel = os.getenv("CHANNEL")  # канал для парсинга

# создаём клиент Telegram
client = TelegramClient("parser_session", api_id, api_hash)


# ------------------------------
# 🧠 ИЗВЛЕЧЕНИЕ ЗАГОЛОВКА
# ------------------------------
def extract_title(text):
    # берём первую строку сообщения как заголовок
    return text.split("\n")[0][:200]


# ------------------------------
# 🔗 СОЗДАНИЕ SLUG
# ------------------------------
def make_slug(text):
    # делаем URL-дружественный slug
    return slugify(text)[:50]


# ------------------------------
# 🛡 ПРОВЕРКА СУЩЕСТВОВАНИЯ ПОСТА
# ------------------------------
@sync_to_async
def blog_exists(slug):
    # проверяем, есть ли уже пост с таким slug
    return Blog.objects.filter(slug=slug).exists()


# ------------------------------
# 💾 СОЗДАНИЕ ПОСТА
# ------------------------------
@sync_to_async
def create_blog(title, content, slug):
    # создаём запись в базе данных
    return Blog.objects.create(
        title=title,
        content=content,
        slug=slug,
        published=True  # сразу публикуем
    )


# ------------------------------
# 🚀 ОСНОВНАЯ ЛОГИКА ПАРСЕРА
# ------------------------------
async def parse():
    # запускаем Telegram клиент
    await client.start()

    print("🚀 Парсер запущен...")

    # перебираем последние сообщения канала
    async for message in client.iter_messages(channel, limit=10):

        # пропускаем сообщения без текста
        if not message.text:
            continue

        # ------------------------------
        # ✂️ ОБРАБОТКА ДАННЫХ
        # ------------------------------
        title = extract_title(message.text)
        content = message.text
        slug = make_slug(title)

        # ------------------------------
        # 🛡 ЗАЩИТА ОТ ДУБЛЕЙ
        # ------------------------------
        if await blog_exists(slug):
            continue

        # ------------------------------
        # 💾 СОХРАНЕНИЕ В БАЗУ
        # ------------------------------
        await create_blog(title, content, slug)

        print("✅ Добавлено:", title)
