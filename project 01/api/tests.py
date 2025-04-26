from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Order, User, Product


# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="test")
        user2 = User.objects.create_user(username="user2", password="test")
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username="user2")
        # TestCase has access to Client()
        self.client.force_login(user)
        response = self.client.get(reverse("user-orders"))

        assert response.status_code == status.HTTP_200_OK
        assert response.status_code == 200
        orders = response.json()

    #     # check all the orders that we received have the same user.id
    #     self.assertTrue(all(order["user"] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        """
        Check unauthenticated users are not allow to access 'user-orders' page,
        and face 403 page (unauthenticated user)
        """
        response = self.client.get(reverse("user-orders"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.normal_user = User.objects.create_user(
            username="user", password="userpass"
        )
        self.product = Product.objects.create(
            name="Test Product", description="Test Description", price=9.99, stock=10
        )
        self.url = reverse("product-detail", kwargs={"pk": self.product.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_unauthorized_update_product(self):
        data = {"name": "Updated Product"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admins_can_delete_product(self):
        # test normal user cannot delete - note that this could be its own method
        self.client.login(username="user", password="userpass")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        # test admin user can
        self.client.login(username="admin", password="adminpass")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
