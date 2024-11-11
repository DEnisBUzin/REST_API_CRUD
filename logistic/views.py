#TODO: Необходимо реализовать пагинацию для вывода списков.

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
    #TODO: Сделать поиск складов, в которых есть определенный продукт, по идентификатору
    pass


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
    # при необходимости добавьте параметры фильтрации
