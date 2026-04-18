import os
import django
import re
from telethon import TelegramClient
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from django.utils.text import slugify

# ------------------------------
# Django setup
# ------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from shop.models import Blog

# ------------------------------
# ENV
# ------------------------------
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
channel = os.getenv("CHANNEL")

client = TelegramClient("parser_session", api_id, api_hash)

# ------------------------------
# CLEAN TEXT
# ------------------------------
def extract_title(text):
    return text.split("\n")[0][:200]


def extract_content(text):
    return text


def make_slug(text):
    return slugify(text)[:50]


# ------------------------------
# DB OPERATIONS (ASYNC SAFE)
# ------------------------------
@sync_to_async
def blog_exists(slug):
    return Blog.objects.filter(slug=slug).exists()


@sync_to_async
def create_blog(title, content, slug):
    return Blog.objects.create(
        title=title,
        content=content,
        slug=slug
    )


# ------------------------------
# PARSER
# ------------------------------
async def parse():
    await client.start()
    print("🚀 Парсер запущен...")

    async for message in client.iter_messages(channel, limit=10):

        if not message.text:
            continue

        title = extract_title(message.text)
        content = extract_content(message.text)
        slug = make_slug(title)

        # защита от дублей
        if await blog_exists(slug):
            continue

        await create_blog(title, content, slug)

        print("✅ Добавлено:", title)


with client:
    client.loop.run_until_complete(parse())