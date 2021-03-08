from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet

from datetime import datetime

from sales_accounting.models import Product, Warehouse
from sales_accounting.serializers import WarehouseSerializer


class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name_warehouse']
    search_fields = ['products']
    ordering_fields = ['pk', 'name_warehouse']

    def create(self, request, *args, **kwargs):
        id_product = request.data['products']
        if Product.objects.filter(pk=id_product).exists():
            name_warehouse = request.data['name_warehouse']
            date = str(request.data['receipt_date']).split('-')
            date = datetime(int(date[0]), int(date[1]), int(date[2])).date()
            count_product = request.data['count_product']
            warehouse = Warehouse.objects.create(name_warehouse=name_warehouse,
                                                 receipt_date=date,
                                                 count_product=count_product)
            warehouse.products.add(id_product)
            return JsonResponse(data={'name_warehouse': name_warehouse, 'products': id_product,
                                      'count': count_product,
                                      'date': date},
                                status=HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(data={'response': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST, safe=False)

    def update(self, request, pk=None):
        id_warehouse = int(pk)
        if Warehouse.objects.filter(pk=id_warehouse).exists():
            count = request.data['count_product']
            product = request.data['products']
            Warehouse.objects.filter(pk=id_warehouse).update(name_warehouse=request.data['name_warehouse'],
                                                             count_product=count)
            return JsonResponse(data={'id_warehouse': id_warehouse,
                                      'name_warehouse': request.data['name_warehouse'],
                                      'products': product,
                                      'count_product': count},
                                status=HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(data={'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST, safe=False)

    def destroy(self, request, pk=None):
        if Warehouse.objects.filter(pk=pk).exists():
            warehouse = Warehouse.objects.get(pk=int(pk))
            warehouse.delete()
            return JsonResponse(data={'id_warehouse': pk}, status=HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data={'id_warehouse': pk}, status=HTTP_404_NOT_FOUND, safe=False)
