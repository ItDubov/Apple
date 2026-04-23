from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.utils.text import slugify
import uuid


# ------------------------------
# 📁 CATEGORY
# ------------------------------
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        cache.delete("categories")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ------------------------------
# 📱 PRODUCT (основа 3D магазина)
# ------------------------------
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField(blank=True)

    # ------------------------------
    # 🎨 ВАРИАНТЫ (важно для будущего UI)
    # ------------------------------
    color = models.CharField(max_length=50, blank=True)
    memory = models.CharField(max_length=50, blank=True)

    # ------------------------------
    # 💰 ЦЕНЫ
    # ------------------------------
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(null=True, blank=True)

    # ------------------------------
    # ⚙️ ГИБКОСТЬ (для 3D и характеристик)
    # ------------------------------
    characteristics = models.JSONField(blank=True, null=True)

    # ------------------------------
    # 🖼️ МЕДИА
    # ------------------------------
    image = models.URLField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    # 🔥 ВАЖНО ДЛЯ ТВОЕГО 3D:
    model_3d = models.URLField(blank=True, null=True)
    # сюда потом будешь класть .glb модели

    # ------------------------------
    # 📊 СТАТУС
    # ------------------------------
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        cache.delete("products")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ------------------------------
# 🛒 ORDER
# ------------------------------
class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_cost(self):
        return sum(item.price * item.quantity for item in self.items.all())


# ------------------------------
# 📦 ORDER ITEM
# ------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


# ------------------------------
# 📝 BLOG
# ------------------------------
class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ------------------------------
# 🖼️ PRODUCT IMAGES
# ------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Image of {self.product.name}"
