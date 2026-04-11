from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'address', 'house', 'apartment', 'comment', 'total_price', 'status', 'created_at')
    search_fields = ('full_name', 'phone', 'address')
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__full_name', 'product__name')
    list_filter = ('order__status',)