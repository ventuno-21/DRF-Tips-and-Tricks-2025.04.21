import django_filters
from api.models import Product


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
