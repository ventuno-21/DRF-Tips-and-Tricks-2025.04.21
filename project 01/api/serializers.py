import datetime
import time

from django.db import transaction
from rest_framework import serializers
from rest_framework.request import Request

from .models import Order, OrderItem, Product, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "password",
            "user_permissions",
            "is_authenticated",
            "get_full_name",
            "orders",
        )
        # exclude = ('password', 'user_permissions')
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        we populate the fields that have relationship wth other tables
        All detail of Foreignkey fileds will be displayed
        instead of just showing an "id"
        """
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        # print("self.context ===", self.context)
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


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


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ("product", "quantity")

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)
    """
    When we want to aupdate another field like status, if we don't send
    items, we will face a problem, therefore, we declare that require=False for
    items filed, so we will be able to update others fild without sending items
    
    """

    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop("items")

        with transaction.atomic():
            """
            with transaction.atomic() we prevent that our order get partially updated
            """

            instance = super().update(instance, validated_data)

            if orderitem_data is not None:
                # Clear existing items (optional, depends on requirements)
                instance.items.all().delete()

                # Recreate items with the updated data
                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance

    def create(self, validated_data):
        # output = {'status': 'Pending', 'items': [{'product': <Product: Digital Camera>, 'quantity': 3}, {'product': <Product: Television>, 'quantity': 3}], 'user': <User: admin>}
        print("validated_data ===== ", validated_data)
        orderitem_data = validated_data.pop("items")
        # output = {'status': 'Pending', 'user': <User: admin>}
        print("validated_data ===== ", validated_data)
        # output =  [{'product': <Product: Digital Camera>, 'quantity': 3}, {'product': <Product: Television>, 'quantity': 3}]
        print("orderitem_data ===== ", orderitem_data)

        with transaction.atomic():

            # the below two line are the same
            # order = Order.objects.create(**validated_data)
            order = Order.objects.create(
                status=validated_data.get("status"), user=validated_data.get("user")
            )

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)

        return order

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "status",
            "items",
        )
        extra_kwargs = {"user": {"read_only": True}}


class OrderSerializer(serializers.ModelSerializer):

    order_id = serializers.UUIDField(read_only=True)
    # status = serializers.Charfield(read_only=True)
    """
    Because read_only is Ture, it wont show up in create form, 
    """

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

    date = serializers.SerializerMethodField(method_name="get_time")

    def get_time(self, obj):
        obj1 = obj.created_at
        return obj1.strftime("Date: %Y-%m-%d - Time: %H:%M:%S")

    class Meta:
        model = Order
        fields = (
            "order_id",
            "date",
            "created_at",
            "user",
            "status",
            "items",
            "total_price",
        )
        extra_kwargs = {"user": {"read_only": True}}


class ProductInfoSerializer(serializers.Serializer):
    """
    Its not a "ModelSerailizer", so we dont use 'Meta' class to declare our Model
    Declaring a serializer looks very similar to declaring a form

    """

    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
