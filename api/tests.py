from django.test import TestCase
from api.models import Order, User
from django.urls import reverse
from rest_framework import status


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
        # check all the orders that we received have the same user.id
        self.assertTrue(all(order["user"] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        """
        Check unauthenticated users are not allow to access 'user-orders' page,
        and face 403 page (unauthenticated user)
        """
        response = self.client.get(reverse("user-orders"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
