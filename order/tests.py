from django.test import TestCase
from django.contrib.auth.models import User
from product.models import Category, Product
from order.serializers import OrderSerializer

class OrderSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="christian", password="123")
        self.category = Category.objects.create(title="Backend", slug="backend")
        self.product1 = Product.objects.create(title="Django Pro", price=100)
        self.product1.category.add(self.category)
        self.product2 = Product.objects.create(title="Python Fluente", price=150)
        self.product2.category.add(self.category)

    def test_valid_order_serializer(self):
        data = {
            "user": self.user.id,
            "products_id": [self.product1.id, self.product2.id],
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.product.count(), 2)
        self.assertEqual(serializer.data["total"], 250)

    def test_invalid_order_serializer_missing_fields(self):
        serializer = OrderSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
        self.assertIn("products_id", serializer.errors)
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token

class TestOrderViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="usuario_teste", password="123")
        token = Token.objects.create(user=self.user)
        token.save()

        self.category = Category.objects.create(title="Tecnologia", slug="tecnologia")
        self.product = Product.objects.create(title="Clean Architecture", price=120)
        self.product.category.add(self.category)

    def test_create_order(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = json.dumps({"products_id": [self.product.id], "user": self.user.id})
        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


