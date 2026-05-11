import json
import re

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from urllib.parse import urljoin

from shop.models import Product, Category


BASE_URL = "https://ihomestore.ru"


# ------------------------------
# 🧹 Очистка цены
# ------------------------------
def clean_price(price_text):
    if not price_text:
        return None

    digits = re.sub(r"[^\d]", "", str(price_text))

    return int(digits) if digits else None


# ------------------------------
# 🖼 НОРМАЛИЗАЦИЯ КАРТИНОК
# ------------------------------
def normalize_image(url):
    if not url:
        return None

    url = str(url).strip()

    # фиксим старые пути
    url = url.replace("/appface/uploads/", "/uploads/")

    # если путь относительный
    if url.startswith("/"):
        url = urljoin(BASE_URL, url)

    # защита от мусора
    if not url.startswith("http"):
        return None

    return url


class Command(BaseCommand):
    help = 'Импорт товаров из JSON'

    def handle(self, *args, **kwargs):

        # ------------------------------
        # 📂 Читаем JSON
        # ------------------------------
        with open('products.json', encoding='utf-8') as f:
            data = json.load(f)

        created_count = 0
        updated_count = 0

        # ------------------------------
        # 🔁 Импорт товаров
        # ------------------------------
        for item in data:

            try:
                # ------------------------------
                # 📝 Название
                # ------------------------------
                name = str(item.get("name", "")).strip()

                if not name:
                    continue

                # ------------------------------
                # 💰 Цены
                # ------------------------------
                price = clean_price(item.get("price"))
                discount_price = clean_price(
                    item.get("discount_price")
                )

                # ------------------------------
                # 🖼 Фото
                # ------------------------------
                image = normalize_image(
                    item.get("image")
                )

                # ------------------------------
                # 📦 Категория
                # ------------------------------
                category_name = self.detect_category(name)

                category_slug = (
                    slugify(category_name)
                    or "accessories"
                )

                category, _ = Category.objects.get_or_create(
                    slug=category_slug,
                    defaults={
                        "name": category_name
                    }
                )

                # ------------------------------
                # 🔑 SLUG
                # ------------------------------
                base_slug = (
                    slugify(name)[:70]
                    or "product"
                )

                # ------------------------------
                # 💾 СОЗДАНИЕ / ОБНОВЛЕНИЕ
                # ------------------------------
                product, created = Product.objects.update_or_create(
                    slug=base_slug,
                    defaults={
                        "name": name[:255],
                        "category": category,
                        "price": price or 0,
                        "discount_price": discount_price,
                        "description": name[:1000],
                        "image": image,
                        "source_url": BASE_URL,
                        "available": True,
                    }
                )

                # ------------------------------
                # ✅ ЛОГИ
                # ------------------------------
                if created:
                    created_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Создан: {name}"
                        )
                    )

                else:
                    updated_count += 1

                    self.stdout.write(
                        f"Обновлён: {name}"
                    )

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка товара {name}: {e}"
                    )
                )

        # ------------------------------
        # 🎉 ГОТОВО
        # ------------------------------
        self.stdout.write(
            self.style.SUCCESS(
                f"\n🔥 Готово!"
                f"\nСоздано: {created_count}"
                f"\nОбновлено: {updated_count}"
            )
        )

    # ------------------------------
    # 🧠 CATEGORY DETECTOR
    # ------------------------------
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

        elif (
            "яндекс" in name
            or "станция" in name
            or "homepod" in name
        ):
            return "Умные колонки"

        else:
            return "Аксессуары"
