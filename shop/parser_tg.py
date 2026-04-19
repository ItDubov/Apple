import os
import re
from telethon import TelegramClient
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from django.utils.text import slugify

from shop.models import Blog

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
channel = os.getenv("CHANNEL")

client = TelegramClient("parser_session", api_id, api_hash)


def extract_title(text):
    return text.split("\n")[0][:200]


def make_slug(text):
    return slugify(text)[:50]


@sync_to_async
def blog_exists(slug):
    return Blog.objects.filter(slug=slug).exists()


@sync_to_async
def create_blog(title, content, slug):
    return Blog.objects.create(
        title=title,
        content=content,
        slug=slug,
        published=True
    )


async def parse():
    await client.start()
    print("🚀 Парсер запущен...")

    async for message in client.iter_messages(channel, limit=10):
        if not message.text:
            continue

        title = extract_title(message.text)
        content = message.text
        slug = make_slug(title)

        if await blog_exists(slug):
            continue

        await create_blog(title, content, slug)
        print("✅ Добавлено:", title)
