# ITDubov — Интернет-магазин техники Apple

## 📌 Описание проекта

Веб-приложение интернет-магазина для продажи техники Apple.
Реализованы каталог товаров, корзина, оформление заказа и блог.

## 🚀 Функционал

* Каталог товаров с категориями
* Страница товара (галерея, характеристики)
* Корзина (добавление, удаление, изменение количества)
* Оформление заказа с отправкой email
* Блог
* Контактная форма
* Мультиязычность (RU / EN / LT)
* Динамика через HTMX (без перезагрузки)
* Кэширование страниц и запросов

## 🛠 Технологии

* Python / Django
* SQLite (или PostgreSQL)
* HTMX
* HTML / CSS
* GNU gettext (i18n)

## ⚙️ Установка

```bash
git clone <repo>
cd itDubov
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🔐 Переменные окружения

Создай файл `.env`:

```
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
```

## 📬 Контакты

Автор: Виктор
