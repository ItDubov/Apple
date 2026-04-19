import json  # работа с JSON файлами
import re  # для очистки цены (регулярки)
import uuid  # генерация уникального slug
from django.core.management.base import BaseCommand  # команда Django
from shop.models import Product, Category  # модели
from django.utils.text import slugify  # генерация slug


# ------------------------------
# 🧹 Очистка цены (из строки в число)
# ------------------------------
def clean_price(price_text):
    # если цены нет → возвращаем None
    if not price_text:
        return None

    # убираем всё кроме цифр (₽, $, пробелы и т.д.)
    digits = re.sub(r"[^\d]", "", price_text)

    # превращаем в число
    return int(digits) if digits else None


class Command(BaseCommand):
    # описание команды (видно в manage.py help)
    help = 'Импорт товаров из JSON'

    def handle(self, *args, **kwargs):
        # ------------------------------
        # 📂 Открываем JSON файл
        # ------------------------------
        with open('products.json', encoding='utf-8') as f:
            data = json.load(f)

        # ------------------------------
        # 🔁 Проходим по каждому товару
        # ------------------------------
        for item in data:
            # название товара
            name = item.get("name", "").strip()

            # цены (чистим через функцию)
            price = clean_price(item.get("price", ""))
            discount_price = clean_price(item.get("discount_price", ""))

            # картинка
            image = item.get("image", "")

            # ------------------------------
            # 🧠 Определяем категорию по названию
            # ------------------------------
            category_name = self.detect_category(name)

            # 🛡 если категория не найдена → ставим дефолт
            if not category_name:
                category_name = "Аксессуары"

            # slug категории (URL-safe)
            category_slug = slugify(category_name)

            # если slug не получился (например кириллица)
            if not category_slug:
                category_slug = "accessories"

            # ------------------------------
            # 📁 Получаем или создаём категорию
            # ------------------------------
            category, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={"name": category_name}
            )

            # ------------------------------
            # 🔥 Генерация уникального slug товара
            # ------------------------------
            # базовый slug из названия
            base_slug = slugify(name)[:60] or "product"

            # добавляем уникальный хвост (чтобы не было дублей)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

            # ------------------------------
            # 💾 Создание товара в базе
            # ------------------------------
            Product.objects.create(
                name=name,
                slug=unique_slug,
                category=category,
                price=price or 0,  # если None → 0
                discount_price=discount_price,
                description=name,  # пока используем имя как описание
                image=image,
                source_url="https://appface.store",
            )

            # вывод в консоль
            self.stdout.write(self.style.SUCCESS(f"Добавлен: {name}"))

        # финальное сообщение
        self.stdout.write(self.style.SUCCESS("🔥 Импорт завершён!"))

    # ------------------------------
    # 🧠 Определение категории
    # ------------------------------
    def detect_category(self, name):
        # приводим к нижнему регистру
        name = name.lower()

        # проверяем ключевые слова
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
            # дефолтная категория
            return "Аксессуары"