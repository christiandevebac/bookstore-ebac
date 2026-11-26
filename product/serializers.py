from rest_framework import serializers
from product.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "title",
            "slug",
            "description",
            "active",
        ]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "active",
            "category",
        ]

    def create(self, validated_data):
        categories_data = validated_data.pop("category")
        product = Product.objects.create(**validated_data)
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            product.category.add(category)
        return product
