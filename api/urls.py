from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list),
    path("products/info/", views.product_info),
    path("products/V01", views.product_list_V01),
    path("products/<int:pk>/", views.product_detail),
    path("orders/", views.order_list),
]
