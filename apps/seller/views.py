from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import SellerCategoriesSerializer, CategoryRequestCancelSerializer
from .models import CategoryRequest
from ..users.models import SellerProfile
from ..catalog.permissions import IsSellerOrReadOnly


class CategoryRequestListCreateView(APIView):
    
    permission_classes = [IsSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    
    
    def post(self, request: Request):
        serializer = SellerCategoriesSerializer(date=request.data)
        if serializer.is_valid(raise_exception=True):
            seller, _ = SellerProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    "FullName": request.user.first_name
                }
            )
            
            CategoryRequest.objects.create(
                seller=seller,
                name=serializer.validated_data['name'],
                image=serializer.validated_data.get('image')
            )
            
            return Response(serializer.validated_data)
    
    def get(self, request: Request):
        pass
    

class CategoryRequestDetailView(APIView):
        
    def get_object(self, pk, user):
        return get_object_or_404(CategoryRequest, pk=pk, seller__user=user)
    
    def get(self, request: Request, pk):
        obj = self.get_object(pk, request.user)
        return Response(SellerCategoriesSerializer(obj).data)

    def put(self, request: Request, pk):
        obj = self.get_object(pk, request.user)
        serializer = SellerCategoriesSerializer(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def patch(self, request: Request, pk):
        obj = self.get_object(pk, request.user)
        serializer = CategoryRequestCancelSerializer(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)