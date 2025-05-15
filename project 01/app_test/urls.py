from django.urls import path

from .views import (
    CategoryListAPIView,
    ArticleListAPIView,
    ProductListAPIView,
    NoteListAPIView,
    NoteDetailAPIView,
    ProductDetailAPIView,
    CategoryDetailAPIView,
    ArticleDetailAPIView,
)

urlpatterns = [
    path("cat/", CategoryListAPIView.as_view()),
    path("cat/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    path("blog/", ArticleListAPIView.as_view()),
    path("blog/<int:pk>/", ArticleDetailAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("Notes/", NoteListAPIView.as_view()),
    path("Notes/<int:pk>/", NoteDetailAPIView.as_view()),
]
