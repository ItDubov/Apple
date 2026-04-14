from django.shortcuts import render
from .models import Category, Product, Blog, OrderItem
from django.shortcuts import get_object_or_404
from .cart import Cart
from django.shortcuts import redirect
from .forms import OrderForm
from .utils import send_order_email


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[:8]
    blogs = Blog.objects.filter(published=True).order_by('-created_at')[:4]

    return render(request, 'index.html', {
        'categories': categories,
        'products': products,
        'blogs': blogs
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'product_detail.html', {
        'product': product
    })

def update_price(request, slug):
    product = get_object_or_404(Product, slug=slug)

    memory = request.GET.get('memory')
    color = request.GET.get('color')

    price = product.price

    if memory == '256':
        price += 100
    if memory == '512':
        price += 200

    return render(request, 'partials/price.html', {'price': price})
# Корзина
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')

# Оформление заказа
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )

            send_order_email(order)
            request.session['cart'] = {}

            return render(request, 'success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form})
