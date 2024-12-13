from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all().order_by('id')
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]
    authentication_classes=[TokenAuthentication]

