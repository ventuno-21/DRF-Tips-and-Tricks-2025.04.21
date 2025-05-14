from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Product, Article, Category
from .serializers import (
    ProductsModelSerializer,
    ArticleModelSerializer,
    CategoryModelSerializer,
)

# Create your views here.


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsModelSerializer
