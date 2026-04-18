import json
import re
import uuid
from django.core.management.base import BaseCommand
from shop.models import Product, Category
from django.utils.text import slugify


def clean_price(price_text):
    if not price_text:
        return None
    digits = re.sub(r"[^\d]", "", price_text)
    return int(digits) if digits else None


class Command(BaseCommand):
    help = 'Импорт товаров из JSON'

    def handle(self, *args, **kwargs):
        with open('products.json', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            name = item.get("name", "").strip()

            price = clean_price(item.get("price", ""))
            discount_price = clean_price(item.get("discount_price", ""))
            image = item.get("image", "")

            category_name = self.detect_category(name)

            # 🛡 защита
            if not category_name:
                category_name = "Аксессуары"

            category_slug = slugify(category_name)
            if not category_slug:
                category_slug = "accessories"

            category, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={"name": category_name}
            )

            # 🔥 УНИКАЛЬНЫЙ SLUG (ГЛАВНОЕ ИСПРАВЛЕНИЕ)
            base_slug = slugify(name)[:60] or "product"
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

            Product.objects.create(
                name=name,
                slug=unique_slug,
                category=category,
                price=price or 0,
                discount_price=discount_price,
                description=name,
                image=image,
                source_url="https://appface.store",
            )

            self.stdout.write(self.style.SUCCESS(f"Добавлен: {name}"))

        self.stdout.write(self.style.SUCCESS("🔥 Импорт завершён!"))

    def detect_category(self, name):
        name = name.lower()

        if "iphone" in name:
            return "iPhone"
        elif "watch" in name:
            return "Apple Watch"
        elif "airpods" in name:
            return "AirPods"
        elif "macbook" in name:
            return "MacBook"
        elif "ipad" in name:
            return "iPad"
        elif "imac" in name:
            return "iMac"
        elif "marshall" in name:
            return "Marshall"
        elif "dyson" in name:
            return "Dyson"
        elif "playstation" in name or "ps5" in name:
            return "PlayStation"
        elif "яндекс" in name or "станция" in name:
            return "Умные колонки"
        else:
            return "Аксессуары"
