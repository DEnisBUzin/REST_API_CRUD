from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description'
        ]


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = [
            'product',
            'quantity',
            'price'
        ]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)


    class Meta:
        model = Stock
        fields = [
            'address',
            'positions'
        ]
    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        position = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for pos in position:
            StockProduct.objects.create(stock=stock, **pos)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        position = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # Удаляем текущие связанные записи, чтобы обновить их
        stock.position.all().delete()

        # Создаём новые записи для связанных данных
        for pos in position:
            StockProduct.objects.create(stock=stock, **pos)

        return stock
