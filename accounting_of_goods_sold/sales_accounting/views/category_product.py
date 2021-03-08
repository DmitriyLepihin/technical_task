from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet

from sales_accounting.models import CategoryProduct
from sales_accounting.serializers import CategoryProductSerializer


class CategoryProductViewSet(ModelViewSet):
    queryset = CategoryProduct.objects.all()
    serializer_class = CategoryProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name_category']
    search_fields = ['name_category']
    ordering_fields = ['pk', 'name_category']

    def create(self, request, *args, **kwargs):
        category = request.data['name_category']
        CategoryProduct(name_category=category).save()
        return JsonResponse(data={'name_category': category}, status=HTTP_200_OK, safe=False)

    def destroy(self, request, pk=None):
        if CategoryProduct.objects.filter(pk=int(pk)).exists():
            category = CategoryProduct.objects.get(pk=int(pk))
            category.delete()
            return JsonResponse(data={'id_category': pk}, status=HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data={'id_category': pk}, status=HTTP_404_NOT_FOUND, safe=False)

    def update(self, request, pk=None):
        name_category = request.data['name_category']
        if CategoryProduct.objects.filter(pk=int(pk)).exists():
            CategoryProduct.objects.filter(pk=int(pk)).update(name_category=name_category)
            return JsonResponse(data={'id_category': pk, 'name_category': name_category},
                                status=HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(data={'id_category': pk}, status=HTTP_400_BAD_REQUEST, safe=False)
