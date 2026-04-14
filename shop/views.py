from django.shortcuts import render
from .models import Category, Product, Blog
from django.shortcuts import get_object_or_404


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