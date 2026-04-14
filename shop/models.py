from django.db import models


# 📁 КАТЕГОРИИ
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# 📱 ТОВАРЫ
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    characteristics = models.JSONField(blank=True, null=True)

    image = models.ImageField(upload_to='products/')
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 🛒 ЗАКАЗ
class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}'


    def get_total_cost(self):
        return sum(item.price * item.quantity for item in self.items.all())


# 📦 ПОЗИЦИЯ ЗАКАЗА
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'


# 📝 БЛОГ
class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# 📸 ДОПОЛНИТЕЛЬНЫЕ ИЗОБРАЖЕНИЯ
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'Image for {self.product.name}'
