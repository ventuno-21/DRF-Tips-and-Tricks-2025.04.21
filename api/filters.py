import django_filters
from rest_framework import filters

from api.models import Order, Product


class InStockFilterBackend(filters.BaseFilterBackend):
    """
    You can also provide your own generic filtering backend,
    or write an installable app for other developers to use.

    To do so override BaseFilterBackend, and override the
    .filter_queryset(self, request, queryset, view) method.
    The method should return a new, filtered queryset.

    As well as allowing clients to perform searches and filtering,
    generic filter backends can be useful for restricting which objects
    should be visible to any given request or user.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    """
    Default django filter has some problems like
    1) is case sensetive
    2) for integers you cant use gt or lt (greater than or less than)
    therefore we define our customized filterset
    how to use it?
    insetead od this =>  filterset_fields = ["name", "price"]
    You should use it like this => filterset_class = ProductFilter
    """

    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["exact", "lt", "gt", "range"],
        }


class OrderFilter(django_filters.FilterSet):
    # __date will extract date from created_at
    created_at = django_filters.DateFilter(field_name="created_at__date")

    class Meta:
        model = Order
        fields = {"status": ["exact"], "created_at": ["lt", "gt", "exact"]}
