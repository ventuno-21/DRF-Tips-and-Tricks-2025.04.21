from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import generics
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.serializers import (
    ProductInfoSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from api.models import Product, Order, OrderItem
from .filters import ProductFilter, InStockFilterBackend


class ProductListCreateAPIView(generics.ListCreateAPIView):
    # below two lines are the same, because of what we defined in Product model
    # queryset = Product.objects.filter(in_stock=True)
    # queryset = Product.objects.filter(stock__gt=0)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,  # customized filter, automatically check if product is available in stock
    ]
    ## below line is case sensetive, so we define our default filter function
    # filterset_fields = ["name", "price"]
    filterset_class = ProductFilter  # http://127.0.0.1:8000/products/?price__gt=100
    # http://127.0.0.1:8000/products/?search=vision
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "stock"]

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProducCreateAPIView(generics.CreateAPIView):
    # below two lines are the same, because of what we defined in Product model
    # queryset = Product.objects.filter(in_stock=True)
    model = Product
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """
        "request.data" in serlizer is equal "request.POST.get('name') "in pure django
        """
        print(request.data)
        return super().create()


@api_view(["GET"])
def product_list_v02(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


def product_list_v01(request):
    """
    Output of this function is same as below,
    but without graphic that DRF uses,
    & is just the normal json format
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(
        {"lenght": len(serializer.data), "data": serializer.data},
    )


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


@api_view(["GET"])
def product_detail_v01(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer


@api_view(["GET"])
def order_list_v01(request):
    # orders = Order.objects.all()
    # orders = Order.objects.prefetch_related("items").all()
    # orders = Order.objects.prefetch_related("items", "items__product").all()
    orders = Order.objects.prefetch_related("items__product")
    """
    The result of 4 above lines are the same, 
    but with 3rd & 4th lines we hit the Databse less than 1st * 2nd line, 
    because in OrderSerlizer, we summon OrderItemSerializer (Thats why we use 'items' in prefetch), 
    and in OrderItemSerializer we summon product (Thats why we use 'items__product' in prefetch))
    The amount of hit to database is the same for 3rd & 4th lines
    """
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)


@api_view(["GET"])
def product_info_v01(request):
    products = Product.objects.all()

    # obj_max_price is an object, but max_price becuse we mention what we want in [] is a value
    obj_max_price = products.aggregate(max_price=Max("price"))
    print(f"All maximum price ===== {obj_max_price}")

    max_price = products.aggregate(max_price=Max("price"))["max_price"]
    print(f"maximum price ===== {max_price}")

    serializer = ProductInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": max_price,
        }
    )
    return Response(serializer.data)
