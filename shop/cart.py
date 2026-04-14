from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        self.cart[str(product_id)]['quantity'] = quantity
        self.save()

    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart.keys())

        for product in products:
            item = self.cart[str(product.id)]
            item['product'] = product
            item['total_price'] = product.price * item['quantity']
            yield item

    def get_total_price(self):
        return sum(item['total_price'] for item in self)

    def save(self):
        self.session.modified = True
