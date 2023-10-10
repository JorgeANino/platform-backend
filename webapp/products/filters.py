import django_filters

from webapp.products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = Product
        fields = ["name", "price", "category"]
