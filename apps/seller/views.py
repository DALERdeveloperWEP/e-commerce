from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from .serializers import SellerCategoriesSerializer
from .models import CategoryRequest
from ..users.models import SellerProfile
from ..catalog.permissions import IsSellerOrReadOnly

class CategoryRequestListCreateView(APIView):
    permission_classes = [IsSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    
    @extend_schema(
        request={"multipart/form-data": SellerCategoriesSerializer},
        responses=SellerCategoriesSerializer
    )
    def post(self, request: Request):
        serializer = SellerCategoriesSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        seller, _ = SellerProfile.objects.get_or_create(
            user=request.user,
            defaults={"FullName": request.user.first_name}
        )
        
        instance = serializer.save(seller=seller)
        
        return Response(SellerCategoriesSerializer(instance, context={'request': request}).data)
    
    @extend_schema(responses=SellerCategoriesSerializer(many=True))
    def get(self, request: Request):
        qs = CategoryRequest.objects.filter(seller__user=request.user).order_by('-id')
        serializer = SellerCategoriesSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryRequestDetailView(APIView):
    permission_classes = [IsSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser] 
        
    def get_object(self, pk, user):
        return get_object_or_404(CategoryRequest, pk=pk, seller__user=user)
    
    def get(self, request: Request, pk):
        obj = self.get_object(pk, request.user)
        serializer = SellerCategoriesSerializer(obj, context={'request': request})
        return Response(serializer.data)

    def put(self, request: Request, pk):
        obj = self.get_object(pk, request.user)
        serializer = SellerCategoriesSerializer(
            obj, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    def patch(self, request: Request, pk):
        return self.put(request, pk)
    

