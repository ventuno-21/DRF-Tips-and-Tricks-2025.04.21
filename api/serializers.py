from rest_framework import serializers
from .models import Product, Order, OrderItem
from rest_framework.request import Request


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            # "id",
            "description",
            "name",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price"
    )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal",
        )


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    """
    Whatever field that is mentioned in OrderItemSerilizer, will be shown in each item
    We can only mention items in our fielsds without bellow line, but then only will show
    the primry_key no, but with above line we populate it
    """

    total_price = serializers.SerializerMethodField(method_name="total")
    """
    we can dont mention method_name and inside the paranteses be empty
    if we do that our metho should start with '_get_<filed_name>'
    that would be like => 'def get_total_price(self, obj)
    but instead of that we used 'method_name' in above line
    """

    # user doesnt have a link yet, so below lines will be check later
    # user = serializers.HyperlinkedIdentityField(view_name="user-list")
    # user = serializers.HyperlinkedRelatedField(read_only=True, view_name="track-detail")

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            "order_id",
            "created_at",
            "user",
            "status",
            "items",
            "total_price",
        )


class ProductInfoSerializer(serializers.Serializer):
    """
    Its not a "ModelSerailizer", so we dont use 'Meta' class to declare our Model
    Declaring a serializer looks very similar to declaring a form

    """

    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
