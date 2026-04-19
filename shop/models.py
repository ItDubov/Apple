from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.utils.text import slugify
import uuid


# ------------------------------
# 📁 МОДЕЛЬ КАТЕГОРИИ
# ------------------------------
class Category(models.Model):
    # название категории (уникальное)
    name = models.CharField(max_length=255, unique=True)

    # slug для URL (например /category/iphone/)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        # перевод названий модели (используется в админке)
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def save(self, *args, **kwargs):
        # если slug не задан — генерируем автоматически
        if not self.slug:
            self.slug = slugify(self.name)

        # сбрасываем кэш категорий (чтобы обновились на сайте)
        cache.delete("categories")

        super().save(*args, **kwargs)

    def __str__(self):
        # отображение в админке
        return self.name


# ------------------------------
# 📱 МОДЕЛЬ ТОВАРА
# ------------------------------
class Product(models.Model):
    # связь с категорией (один ко многим)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    # название товара
    name = models.CharField(max_length=255)

    # уникальный slug для страницы товара
    slug = models.SlugField(unique=True, blank=True)

    # дополнительные характеристики (необязательные)
    memory = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)

    # описание товара
    description = models.TextField(blank=True)

    # ------------------------------
    # 💰 ЦЕНЫ
    # ------------------------------
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(null=True, blank=True)

    # JSON поле для гибких характеристик (например: {"cpu": "M1"})
    characteristics = models.JSONField(blank=True, null=True)

    # изображение как URL (не файл — удобно для парсинга)
    image = models.URLField(blank=True, null=True)

    # ссылка на источник (например сайт-парсер)
    source_url = models.URLField(blank=True, null=True)

    # доступность товара
    available = models.BooleanField(default=True)

    # дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # сортировка по дате (новые сверху)
        ordering = ["-created_at"]

        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def save(self, *args, **kwargs):
        # генерация slug если не задан
        if not self.slug:
            self.slug = slugify(self.name)

        # сброс кэша товаров
        cache.delete("products")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# ------------------------------
# 🛒 МОДЕЛЬ ЗАКАЗА
# ------------------------------
class Order(models.Model):
    # данные клиента
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    address = models.TextField()

    # дата создания заказа
    created_at = models.DateTimeField(auto_now_add=True)

    # статус оплаты
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}'

    # подсчет общей суммы заказа
    def get_total_cost(self):
        return sum(item.price * item.quantity for item in self.items.all())


# ------------------------------
# 📦 ПОЗИЦИЯ ЗАКАЗА
# ------------------------------
class OrderItem(models.Model):
    # связь с заказом
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    # товар
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # цена на момент покупки
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # количество
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'


# ------------------------------
# 📝 МОДЕЛЬ БЛОГА
# ------------------------------
class Blog(models.Model):
    # заголовок поста
    title = models.CharField(max_length=255)

    # slug для URL статьи
    slug = models.SlugField(unique=True, blank=True)

    # содержимое статьи
    content = models.TextField()

    # изображение (загружается в media/blog)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    # дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    # опубликован ли пост
    published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # создаём уникальный slug (чтобы не было конфликтов)
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ------------------------------
# 📸 ДОПОЛНИТЕЛЬНЫЕ ИЗОБРАЖЕНИЯ ТОВАРА
# ------------------------------
class ProductImage(models.Model):
    # связь с товаром
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    # ссылка на изображение
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'Image for {self.product.name}'
