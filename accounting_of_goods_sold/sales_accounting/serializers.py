from rest_framework.serializers import ModelSerializer

from sales_accounting.models import CategoryProduct, Product, Warehouse, Shop, SalesAccounting


class CategoryProductSerializer(ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class SalesAccountingSerializer(ModelSerializer):
    class Meta:
        model = SalesAccounting
        fields = '__all__'
