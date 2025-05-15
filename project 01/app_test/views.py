from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Product, Article, Category, Note
from .serializers import (
    ProductsModelSerializer,
    ArticleModelSerializer,
    CategoryModelSerializer,
    NoteModelSerializer,
)

# Create your views here.


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer


class ArticleDetailAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsModelSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsModelSerializer


class NoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteModelSerializer


class NoteDetailAPIView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteModelSerializer
