from django.test import TestCase
from shop.models import Product, Category

class ProductTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="iPhone", slug="iphone")

    def test_product_create(self):
        product = Product.objects.create(
            category=self.category,
            name="iPhone 15",
            slug="iphone-15",
            description="Test",
            price=1000
        )

        self.assertEqual(product.name, "iPhone 15")
