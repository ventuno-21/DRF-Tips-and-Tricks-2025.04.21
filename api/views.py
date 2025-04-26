from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from api.models import Order, OrderItem, Product, User
from api.serializers import (
    OrderCreateSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
    UserSerializer,
)

from .filters import InStockFilterBackend, OrderFilter, ProductFilter


class ProductListCreateAPIView(generics.ListCreateAPIView):
    throttle_scope = "products"
    throttle_classes = [ScopedRateThrottle]
    # below two lines are the same, because of what we defined in Product model
    # queryset = Product.objects.filter(in_stock=True)
    # queryset = Product.objects.filter(stock__gt=0)
    queryset = Product.objects.order_by("pk")
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

    pagination_class = PageNumberPagination
    pagination_class.page_size = 10  # This will override what we define in settings
    ## instead of 127.0.0.1:8000/products/?page=3 will be  127.0.0.1:8000/products/?pagenum=3
    pagination_class.page_query_param = "pagenum"
    pagination_class.page_size_query_param = 10
    """ 
    with query size=number it will override our page_size and the quantity of objects
    that will retun will be equal 'number, 
    therefore if we dont mention what page_size_query_param clinet can access
    and a client mention vey large number like size=1000000000 it would be bad for 
    our databse
    Thats why we should mention => pagination_class.page_size_query_param = 10
    """

    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def list(self, request, *arges, **kwargs):
        """
        response to to this url will becached in redis,
        1st attempt too this url will take 5 seconds, because we mention to sleep
        for 2 seconds in get_queryset() methods,
        but 2nd attempt to this url will be so fast because we cached the response in redis

        why we use caching?
        1) avoid hitting database as much as possible in time that we mention which is(15 minunets=60*15)
        2) we we go to same url will be in fast approach
        3) is better to use for databases that wont change more frequently

        what is the problem of caching?
        If we update database or change sth in our related view or serlizer,
        or whatever that is related to this url, for amount of time that we mention
        will not change, (amount of time =15 minutes thet we mention in decorator)

        how to solve this problem?
        A signal has been wroten, in case the table related to this URL is changed, delete previous cach
        """
        return super().list(request, *arges, **kwargs)

    def get_queryset(self):
        import time

        time.sleep(5)
        return super().get_queryset()

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


class OrderViewSet(viewsets.ModelViewSet):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "orders"
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    @method_decorator(cache_page(60 * 15, key_prefix="order_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *arges, **kwargs):
        """
        response to to this url will becached in redis,
        1st attempt too this url will take 5 seconds, because we mention to sleep
        for 2 seconds in get_queryset() methods,
        but 2nd attempt to this url will be so fast because we cached the response in redis

        why we use caching?
        1) avoid hitting database as much as possible in time that we mention which is(15 minunets=60*15)
        2) we we go to same url will be in fast approach
        3) is better to use for databases that wont change more frequently

        what is the problem of caching?
        1) If we update database or change sth in our related view or serlizer,
        or whatever that is related to this url, for amount of time that we mention
        will not change, (amount of time =15 minutes thet we mention in decorator)
        how to solve this problem?
        A signal has been wroten, in case the table related to this URL is changed, delete previous cache
        2) if we dont use proper header when we send a request, it will send the other
        users that use the same URL for us too.
        how to solve this problem?
        we can use decorator like vary_on_headers or vary_on_cookie
        we use @method_decorator(vary_on_headers("Authorization"))
        because each user has a specific token
        """
        return super().list(request, *arges, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """
        we want to use diiferent serializer
        if the self.request.method="post" or the action=="create"
        Also we have to declare create & update method in related serializer
        """
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """only users that own the order & admin are able to see/edit/delete the order"""
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # @action(
    #     detail=False,
    #     methods=["get"],
    #     url_path="user-orders",
    #     permission_classes=[IsAuthenticated],
    # )
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.ge t_serializer(orders, many=True)
    #     return Response(serializer.data)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination


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


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
