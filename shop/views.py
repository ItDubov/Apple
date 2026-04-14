from django.shortcuts import render
from .models import Category, Product, Blog


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[:8]
    blogs = Blog.objects.filter(published=True).order_by('-created_at')[:4]

    return render(request, 'index.html', {
        'categories': categories,
        'products': products,
        'blogs': blogs
    })
