from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListAPIView.as_view()),
    path("products/v02", views.product_list_v02),
    path("products/V01", views.product_list_v01),
    path("products/info/", views.product_info),
    path("products/v01/<int:pk>/", views.product_detail_v01),
    path("products/<int:pk>/", views.ProductDetailAPIView.as_view()),
    path("orders/", views.OrderListAPIView.as_view()),
    path("orders/v01/", views.order_list_v01),
]
