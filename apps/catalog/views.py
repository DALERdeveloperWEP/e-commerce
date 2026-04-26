from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework_simplejwt.authentication import JWTAuthentication

from core.services import MyPagination
from .models import Category, Product, Favorite 
from .serializers import (
    CategorySerailzer, 
    ProductSerailzer, 
    FavoritSerailzer, 
    UniversalCategorySerializer, 
    CategoryUpdateSerializser,
    CategoryDeleteSerializser
)
from .permissions import IsSellerOrReadOnly, IsUserOrReadOnly, IsOwnerOrReadOnly, IsAdminOrReadOnly
from ..seller.models import CategoryRequest

@extend_schema(tags=['Catalog'])
class CategoryViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CategorySerailzer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    http_method_names = ['get', 'post', 'put', 'patch']
    
    def get_object(self):
        
        obj_id = self.kwargs.get('pk')
        
        obj = CategoryRequest.objects.filter(id=obj_id).first()
        if obj:
            return obj
        
        return get_object_or_404(Category, id=obj_id)
    
    @extend_schema(request=UniversalCategorySerializer, responses=UniversalCategorySerializer)
    def list(self, request, *args, **kwargs):
        serializer = UniversalCategorySerializer(list(Category.objects.all()) + list(CategoryRequest.objects.filter(status='completed').all()), many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=UniversalCategorySerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        
        
    @extend_schema(request=CategoryDeleteSerializser, responses={"message": "Muvaffaqiyatli o'chirildi"})
    @action(detail=True, methods=['post'])
    def delete(self, request, pk):
        created_by_type = request.data.get('created_by_type')
        
        if created_by_type == 'seller':
            instance = get_object_or_404(CategoryRequest, id=pk)
        elif created_by_type == 'admin':
            instance = get_object_or_404(Category, id=pk)
        else:
            return Response(
                {"error": "Noto'g'ri created_by_type qiymati. Faqat 'admin' yoki 'seller' bo'lishi mumkin."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response(
            {"message": "Muvaffaqiyatli o'chirildi"}, 
            status=status.HTTP_204_NO_CONTENT
        )
      
    
    @extend_schema(responses=UniversalCategorySerializer)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        
    @extend_schema(request=CategoryUpdateSerializser, responses=UniversalCategorySerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(request=CategoryUpdateSerializser, responses=UniversalCategorySerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    


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
    