from django.db import models

# Create your models here.
from api.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"category: {self.name}"


class Article(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="article_category"
    )
    description = models.TextField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"Article: {self.title}"


class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="product_category"
    )
    description = models.TextField(max_length=100, blank=True, null=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"Product: {self.name}"


class Note(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="note_category"
    )
    description = models.TextField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return f"Note: {self.title}"
