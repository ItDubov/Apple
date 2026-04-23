from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.core.mail import send_mail

from .models import Category, Product, Blog, OrderItem
from .cart import Cart
from .forms import OrderForm, ContactForm
from .utils import send_order_email


# ------------------------------
# 🔁 ROOT → LANDING (3D ENTRY POINT)
# ------------------------------
def root(request):
    return redirect('landing')


# ------------------------------
# 🌌 LANDING (первая 3D сцена / вход)
# ------------------------------
def landing(request):
    return render(request, 'landing.html', {
        'hide_header': True
    })


# ------------------------------
# 🏠 HOME (основная 3D сцена / каталог вход)
# ------------------------------
def home(request):
    products = cache.get('products')
    categories = cache.get('categories')
    blogs = cache.get('blogs')

    if products is None:
        products = Product.objects.filter(available=True)
        cache.set('products', products, 60 * 10)

    if categories is None:
        categories = Category.objects.all()
        cache.set('categories', categories, 60 * 60)

    if blogs is None:
        blogs = Blog.objects.filter(published=True).order_by('-created_at')[:4]
        cache.set('blogs', blogs, 60 * 10)

    return render(request, 'home.html', {
        'hide_header': False,
        'products': products,
        'categories': categories,
        'blogs': blogs
    })


# ------------------------------
# 📱 PRODUCT DETAIL
# ------------------------------
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'product_detail.html', {
        'product': product
    })


# ------------------------------
# 💰 PRICE UPDATE (HTMX)
# ------------------------------
def update_price(request, slug):
    product = get_object_or_404(Product, slug=slug)

    memory = request.GET.get('memory')
    price = product.price

    if memory == '256':
        price += 100
    elif memory == '512':
        price += 200

    return render(request, 'partials/price.html', {
        'price': price
    })


# ------------------------------
# 🛒 CART
# ------------------------------
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id)

    return render(request, 'partials/cart_count.html', {
        'cart': cart
    })


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_detail')


# ------------------------------
# 💳 CHECKOUT
# ------------------------------
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

            return render(request, 'success.html', {
                'order': order
            })

    else:
        form = OrderForm()

    return render(request, 'checkout.html', {
        'form': form
    })


# ------------------------------
# 📩 CONTACT
# ------------------------------
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            send_mail(
                subject=f"Сообщение от {data['name']}",
                message=data['message'],
                from_email=data['email'],
                recipient_list=['admin@email.com'],
            )

            return render(request, 'contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form
    })


# ------------------------------
# 📝 BLOG LIST
# ------------------------------
def blog_list(request):
    blogs = Blog.objects.filter(published=True).order_by('-created_at')

    return render(request, 'blog_list.html', {
        'blogs': blogs
    })


# ------------------------------
# 📝 BLOG DETAIL
# ------------------------------
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, published=True)

    return render(request, 'blog_detail.html', {
        'blog': blog
    })


# ------------------------------
# 🔍 PRODUCT FILTER (HTMX)
# ------------------------------
def filter_products(request):
    category_id = request.GET.get('category')

    products = Product.objects.filter(available=True)

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'partials/product_list.html', {
        'products': products
    })


# ------------------------------
# 📂 CATEGORY PAGE
# ------------------------------
def category_view(request, id):
    category = get_object_or_404(Category, id=id)

    products = Product.objects.filter(
        category=category,
        available=True
    )

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })
