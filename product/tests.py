from django.test import TestCase
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer

class CategorySerializerTestCase(TestCase):
    def setUp(self):
        self.category_data = {
            "title": "Tecnologia",
            "slug": "tecnologia",
            "description": "Livros de tecnologia",
            "active": True,
        }

    def test_valid_category_serializer(self):
        serializer = CategorySerializer(data=self.category_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.title, "Tecnologia")

    def test_invalid_category_serializer_missing_required(self):
        serializer = CategorySerializer(data={"description": "Sem titulo e slug"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("slug", serializer.errors)

class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.product_data = {
            "title": "Clean Code",
            "description": "Livro de boas praticas",
            "price": 120,
            "active": True,
            "category": [
                {
                    "title": "Programacao",
                    "slug": "programacao",
                    "description": "Desenvolvimento de software",
                    "active": True,
                }
            ],
        }

    def test_valid_product_serializer_with_category(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.title, "Clean Code")
        self.assertEqual(product.category.count(), 1)
        self.assertEqual(serializer.data["category"][0]["title"], "Programacao")

    def test_invalid_product_serializer(self):
        serializer = ProductSerializer(data={"price": -50})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("category", serializer.errors)
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestProductViewSet(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Romance", slug="romance")
        self.product = Product.objects.create(title="Dom Casmurro", price=50)
        self.product.category.add(self.category)

    def test_get_all_product(self):
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)
        self.assertEqual(product_data["results"][0]["title"], self.product.title)



    def test_create_product(self):
        data = json.dumps({
            "title": "O Cortico",
            "price": 45,
            "category": [{"title": "Literatura", "slug": "literatura"}],
        })
        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestCategoryViewSet(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Ficcao", slug="ficcao")

    def test_get_all_category(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)
        self.assertEqual(category_data["results"][0]["title"], self.category.title)



    def test_create_category(self):
        data = json.dumps({"title": "Biografia", "slug": "biografia"})
        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

