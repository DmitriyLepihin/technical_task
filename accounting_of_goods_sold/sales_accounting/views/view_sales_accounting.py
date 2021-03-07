from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from sales_accounting.models import SalesAccounting
from sales_accounting.serializers import SalesAccountingSerializer


class SalesAccountingViewSet(ModelViewSet):
    serializer_class = SalesAccountingSerializer
    queryset = SalesAccounting

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return JsonResponse(serializer.data, status=HTTP_200_OK, safe=False)
