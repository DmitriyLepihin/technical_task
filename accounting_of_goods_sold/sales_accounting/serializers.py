from django.contrib.auth.models import User
from rest_framework import serializers
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


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
