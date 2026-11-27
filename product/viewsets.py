from rest_framework.viewsets import ModelViewSet
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all().order_by("id")

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by("id")
