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
