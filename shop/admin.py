from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Blog, ProductImage
from django.utils.html import format_html


# 📁 CATEGORY
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

# 📱 PRODUCT
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_preview', 'category', 'price', 'available', 'created_at')
    list_filter = ('available', 'category', 'created_at')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return '-'

    image_preview.short_description = 'Image'


# 📦 ORDER ITEM INLINE
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# 🛒 ORDER
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'paid', 'created_at', 'total_cost')
    list_filter = ('paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [OrderItemInline]


    def total_cost(self, obj):
        return obj.get_total_cost()

    total_cost.short_description = 'Total'


# 📝 BLOG
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published', 'created_at')
    list_filter = ('published',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
