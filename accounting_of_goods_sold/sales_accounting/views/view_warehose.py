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

    def list(self, request, *args, **kwargs):
        if request.query_params.get('search'):
            self.queryset = self.queryset.filter(products=request.query_params.get('search'))
            if self.queryset:
                return JsonResponse(data=list(self.queryset.values()), status=HTTP_200_OK,
                                    safe=False)
            else:
                return JsonResponse(data={'search': request.query_params.get('search')},
                                    status=HTTP_404_NOT_FOUND,
                                    safe=False)
        elif request.query_params.get('ordering'):
            self.queryset = self.queryset.order_by(request.query_params.get('ordering'))
            if self.queryset:
                return JsonResponse(data=list(self.queryset.values()), status=HTTP_200_OK, safe=False)
            else:
                return JsonResponse(data={'ordering': request.query_params.get('ordering')},
                                    status=HTTP_404_NOT_FOUND,
                                    safe=False)
        elif request.query_params.get('name_warehouse'):
            self.queryset = self.queryset.filter(name_warehouse=request.query_params.get('name_warehouse'))
            if self.queryset:
                return JsonResponse(data=list(self.queryset.values()), status=HTTP_200_OK, safe=False)
            else:
                return JsonResponse(data={'name_warehouse': request.query_params.get('name_warehouse')},
                                    status=HTTP_404_NOT_FOUND,
                                    safe=False)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
            return JsonResponse(serializer.data, status=HTTP_200_OK, safe=False)

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
