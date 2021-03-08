from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet

from sales_accounting.models import CategoryProduct, Product
from sales_accounting.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name_product']
    search_fields = ['category_product_id']
    ordering_fields = ['pk', 'name_category', 'category_product_id']

    def create(self, request, *args, **kwargs):
        id_category = request.data['category_product_id']
        name_product = request.data['name_product']
        if CategoryProduct.objects.filter(pk=id_category).exists():
            product = Product(category_product_id_id=id_category, name_product=name_product)
            product.save()
            return JsonResponse(data={'category_product_id': id_category, 'name_product': name_product},
                                status=HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(data={'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST, safe=False)

    def update(self, request, pk=None):
        id_category = request.data['category_product_id']
        if Product.objects.filter(pk=int(pk)).exists() and CategoryProduct.objects.filter(pk=id_category).exists():
            category_product = CategoryProduct.objects.get(pk=id_category)
            name_product = request.data['name_product']

            Product.objects.filter(pk=int(pk)).update(name_product=name_product,
                                                      category_product_id_id=category_product.pk)
            return JsonResponse(data={'name_product': name_product, 'product_category_id': id_category},
                                status=HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(data={'response': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST, safe=False)

    def destroy(self, request, pk=None):
        if Product.objects.filter(pk=int(pk)).exists():
            category = Product.objects.get(pk=int(pk))
            category.delete()
            return JsonResponse(data={'id_product': pk}, status=HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data={'id_product': pk}, status=HTTP_404_NOT_FOUND, safe=False)
