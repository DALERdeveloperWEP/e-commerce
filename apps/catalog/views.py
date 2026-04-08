from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from .models import Category, Product, Favorite 
from .serializers import CategorySerailzer, ProductSerailzer, FavoritSerailzer
from .permissions import IsSellerOrReadOnly, IsUserOrReadOnly, IsOwnerOrReadOnly

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
    permission_classes = [IsUserOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    