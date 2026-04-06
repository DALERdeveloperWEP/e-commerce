from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from .models import Category, Product, Favorite 
from .serializers import CategorySerailzer, ProductSerailzer, FavoritSerailzer
from .permissions import IsSellerOrReadOnly, IsUserOrReadOnly

@extend_schema(tags=['Catalog'])
class CategoryViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CategorySerailzer
    queryset = Category.objects.all()
    permission_classes = [IsSellerOrReadOnly]


@extend_schema(tags=['Product'])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerailzer
    permission_classes = [IsSellerOrReadOnly]


@extend_schema(tags=['Favorite'])
class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoritSerailzer
    queryset = Favorite.objects.all()
    permission_classes = [IsUserOrReadOnly]