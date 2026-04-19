from django.core.management.base import BaseCommand
from shop.parser_tg import parse
import asyncio


class Command(BaseCommand):
    help = "Parse Telegram channel"

    def handle(self, *args, **kwargs):
        asyncio.run(parse())
