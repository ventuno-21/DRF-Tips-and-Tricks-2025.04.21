from django.contrib import admin
from .models import Category, Article, Product, Note

# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Product)
admin.site.register(Note)
