from django.urls import path

from .views import (
    CategoryListAPIView,
    ArticleListAPIView,
    ProductListAPIView,
    NoteListAPIView,
    NoteDetailAPIView,
    ProductDetailAPIView,
)

urlpatterns = [
    path("cat/", CategoryListAPIView.as_view()),
    path("blog/", ArticleListAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("Notes/", NoteListAPIView.as_view()),
    path("Notes/<int:pk>/", NoteDetailAPIView.as_view()),
]
