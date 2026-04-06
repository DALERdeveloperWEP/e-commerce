from rest_framework.serializers import ModelSerializer

from rest_framework import serializers
from .models import Category, Product, Favorite 



class CategorySerailzer(ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Category
        fields = ['name', 'image', 'slug']
        read_only_fields = ['slug']
        


class ProductSerailzer(ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Product
        fields = '__all__'
    


class FavoritSerailzer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['product']
        read_only_fields = ['user']