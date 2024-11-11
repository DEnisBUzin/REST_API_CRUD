import django_filters
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['title',
                  'description']


class StockFilter(django_filters.FilterSet):
    products = django_filters.NumberFilter(field_name='positions__product__id')
    name_product = django_filters.CharFilter(field_name='positions__product__title',
                                             lookup_expr='icontains')
    description_product = django_filters.CharFilter(field_name='description__product__description',
                                                    lookup_expr='icontains')

    class Meta:
        model = Stock
        fields = ['products',
                  'name_product',
                  'description_product'
                  ]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Параметры фильтрации
    filter_backends = [DjangoFilterBackend,
                       SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title',
                     'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    # параметры фильтрации
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter
