from django.contrib import admin

from .models import Category, Product, Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    create_fieldsets = (
        (None, {
            'fields': ('name', 'image')
        }),
    )
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discount_price', 'stock', 'is_available')
    search_fields = ('title', 'brand', 'country')
    list_filter = ('is_available', 'brand', 'country')
    

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('user__username', 'product__title')
    list_filter = ('user', 'product')
    

