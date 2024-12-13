from django.shortcuts import render
from .serializers import CategorySerializer
from .models import Category
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all().order_by('-created_at')
    serializer_class=CategorySerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[AllowAny]
    
    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

