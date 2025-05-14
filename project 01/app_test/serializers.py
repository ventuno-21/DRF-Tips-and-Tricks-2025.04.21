from rest_framework import serializers
from .models import Category, Article, Product


class CategoryModelSerializer(serializers.ModelSerializer):
    """
    Prodcut & Article models, have a foreignkey relationship with Category Table,

    the related_name of category field in Article Model/table is artcile_category
    the related_name of category field in Product Model/table is product_category

    to show the __str__ method of Product & Article table in categorySerilizer, we should mention:
    <related_name>=serlizers.StringRelatedField(many=true)

    or
    serializers.StringRelatedField(many=True)
    """

    article_category = serializers.StringRelatedField(many=True)
    product_category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = "__all__"


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ProductsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
