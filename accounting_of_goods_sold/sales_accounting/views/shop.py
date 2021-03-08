from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet

from sales_accounting.models import Product, Warehouse, Shop
from sales_accounting.serializers import ShopSerializer


class ShopViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name_shop']
    search_fields = ['id_product']
    ordering_fields = ['pk', 'name_shop']

    def create(self, request, *args, **kwargs):
        id_warehouses = request.data['id_warehouses']
        id_product = request.data['id_product']
        if Shop.objects.filter(warehouses=id_warehouses, id_product=id_product).exists():
            return JsonResponse(data={'msg': 'The product from this warehouse is already being sold by another shop'},
                                status=HTTP_400_BAD_REQUEST,
                                safe=False)
        elif Warehouse.objects.filter(pk=id_warehouses, products=id_product).exists():
            product = Product.objects.get(pk=id_product)
            name_shop = request.data['name_shop']
            price_product = request.data['price_product']
            count = request.data['count']
            shop = Shop.objects.create(name_shop=name_shop,
                                       price_product=price_product,
                                       id_product=product,
                                       count=count,
                                       )
            shop.warehouses.add(id_warehouses)
            return JsonResponse(data={'name_shop': name_shop,
                                      'id_warehouses': id_warehouses,
                                      'id_product': id_product,
                                      'price_product': price_product,
                                      'count': count
                                      },
                                status=HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(data={'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST, safe=False)

    def update(self, request, pk=None):
        shop_id = int(pk)
        if Shop.objects.filter(pk=shop_id).exists():
            count = request.data['count']
            product = request.data['id_product']
            price_product = request.data['price_product']
            Shop.objects.filter(pk=shop_id, id_product=product).update(name_shop=request.data['name_shop'],
                                                                       count=count,
                                                                       price_product=price_product)
            return JsonResponse(data={'id_shop': shop_id,
                                      'name_shop': request.data['name_shop'],
                                      'id_product': product,
                                      'count': count,
                                      'price_product': price_product},
                                status=HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(data={'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST, safe=False)

    def destroy(self, request, pk=None):
        if Shop.objects.filter(pk=pk).exists():
            shop = Shop.objects.get(pk=int(pk))
            shop.delete()
            return JsonResponse(data={'shop_id': pk}, status=HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data={'shop_id': pk}, status=HTTP_404_NOT_FOUND, safe=False)
