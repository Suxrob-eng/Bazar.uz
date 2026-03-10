from django.contrib import admin
from .models import (
    Category, Seller, Product, ProductImage,
    Favorite, Complaint, Cart, CartItem,
    Order, OrderItem, Review
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'icon', 'created_at']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'city', 'region', 'rating', 'total_sales', 'created_at', 'is_active']
    list_filter = ['city', 'region', 'is_active']
    search_fields = ['full_name', 'phone']
    readonly_fields = ['rating', 'total_sales']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'seller', 'price', 'category', 'condition', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'condition', 'category', 'is_bargain']
    search_fields = ['title', 'description']
    readonly_fields = ['views_count']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'is_main', 'created_at']
    list_filter = ['is_main']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'created_at']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'reason', 'created_at']
    list_filter = ['reason']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'created_at', 'updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'city']
    search_fields = ['full_name', 'phone', 'email']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_title', 'product_price', 'quantity']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rating', 'created_at']
    list_filter = ['rating']

