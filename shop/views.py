from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Blog, OrderItem
from .cart import Cart
from .forms import OrderForm, ContactForm
from .utils import send_order_email
from django.core.mail import send_mail
from django.core.cache import cache


# ------------------------------
# 🏠 ГЛАВНАЯ СТРАНИЦА (с кэшированием)
# ------------------------------
def index(request):
    # пробуем получить данные из кэша
    products = cache.get('products')
    categories = cache.get('categories')
    blogs = cache.get('blogs')

    # если товаров нет в кэше → берём из БД
    if not products:
        products = Product.objects.filter(available=True)
        cache.set('products', products, 60 * 10)  # кэш на 10 минут

    # категории кэшируются дольше (редко меняются)
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories, 60 * 60)

    # последние посты блога
    if not blogs:
        blogs = Blog.objects.filter(published=True).order_by('-created_at')[:4]
        cache.set('blogs', blogs, 60 * 10)

    # передаём данные в шаблон
    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'blogs': blogs
    })


# ------------------------------
# 📱 СТРАНИЦА ТОВАРА
# ------------------------------
def product_detail(request, slug):
    # получаем товар по slug или 404
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'product_detail.html', {
        'product': product
    })


# ------------------------------
# 💰 ДИНАМИЧЕСКОЕ ОБНОВЛЕНИЕ ЦЕНЫ (HTMX)
# ------------------------------
def update_price(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # получаем выбранную память из GET
    memory = request.GET.get('memory')

    price = product.price

    # изменяем цену в зависимости от памяти
    if memory == '256':
        price += 100
    elif memory == '512':
        price += 200

    # возвращаем только кусок HTML (partial)
    return render(request, 'partials/price.html', {'price': price})


# ------------------------------
# 🛒 КОРЗИНА
# ------------------------------
def cart_detail(request):
    # создаём объект корзины (через session)
    cart = Cart(request)

    return render(request, 'cart.html', {'cart': cart})


# добавление товара в корзину
def cart_add(request, product_id):
    cart = Cart(request)
    cart.add(product_id=product_id)

    # возвращаем только обновлённый счётчик (HTMX)
    return render(request, 'partials/cart_count.html', {
        'cart': cart
    })


# удаление товара из корзины
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_detail')


# ------------------------------
# 💳 ОФОРМЛЕНИЕ ЗАКАЗА
# ------------------------------
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # сохраняем заказ
            order = form.save()

            # создаём позиции заказа
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )

            # отправка email администратору
            send_order_email(order)

            # очищаем корзину
            request.session['cart'] = {}

            return render(request, 'success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form})


# ------------------------------
# 📩 КОНТАКТНАЯ ФОРМА
# ------------------------------
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # отправка письма
            send_mail(
                subject=f"Сообщение от {data['name']}",
                message=data['message'],
                from_email=data['email'],
                recipient_list=['admin@email.com'],
            )

            return render(request, 'contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ------------------------------
# 📝 СПИСОК БЛОГА
# ------------------------------
def blog_list(request):
    # получаем только опубликованные посты
    blogs = Blog.objects.filter(published=True).order_by('-created_at')

    return render(request, 'blog_list.html', {'blogs': blogs})


# ------------------------------
# 📝 ДЕТАЛЬНАЯ СТРАНИЦА БЛОГА
# ------------------------------
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, published=True)

    return render(request, 'blog_detail.html', {'blog': blog})


# ------------------------------
# 🔍 ФИЛЬТР ТОВАРОВ (HTMX)
# ------------------------------
def filter_products(request):
    # получаем id категории из запроса
    category_id = request.GET.get('category')

    products = Product.objects.filter(available=True)

    # фильтрация по категории
    if category_id:
        products = products.filter(category_id=category_id)

    # возвращаем только список товаров (partial)
    return render(request, 'partials/product_list.html', {
        'products': products
    })


# ------------------------------
# 📂 СТРАНИЦА КАТЕГОРИИ
# ------------------------------
def category_view(request, id):
    # получаем категорию
    category = get_object_or_404(Category, id=id)

    # товары этой категории
    products = Product.objects.filter(category=category, available=True)

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })
