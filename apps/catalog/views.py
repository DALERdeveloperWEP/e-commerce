from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework_simplejwt.authentication import JWTAuthentication

from core.services import MyPagination
from .models import Category, Product, Favorite 
from .serializers import CategorySerailzer, ProductSerailzer, FavoritSerailzer, UniversalCategorySerializer
from .permissions import IsSellerOrReadOnly, IsUserOrReadOnly, IsOwnerOrReadOnly, IsAdminOrReadOnly
from ..seller.models import CategoryRequest

@extend_schema(tags=['Catalog'])
class CategoryViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CategorySerailzer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def get_object(self):
        
        obj_id = self.kwargs.get('pk')
        
        obj = CategoryRequest.objects.filter(id=obj_id).first()
        if obj:
            return obj
        
        return get_object_or_404(Category, id=obj_id)
    
    def list(self, request, *args, **kwargs):
        
        serializer = UniversalCategorySerializer(list(Category.objects.all()) + list(CategoryRequest.objects.filter(status='completed').all()), many=True)
        
        return Response(serializer.data)


@extend_schema(tags=['Product'])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerailzer
    pagination_class = MyPagination
    permission_classes = [IsSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]


@extend_schema(tags=['Favorite'])
class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoritSerailzer
    queryset = Favorite.objects.all()
    pagination_class = MyPagination
    permission_classes = [IsUserOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    