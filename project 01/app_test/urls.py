from django.urls import path

from .views import CategoryListAPIView, ArticleListAPIView, ProductListAPIView

urlpatterns = [
    path("cat/", CategoryListAPIView.as_view()),
    path("blog/", ArticleListAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
]
