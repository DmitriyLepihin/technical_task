"""accounting_of_goods_sold URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from sales_accounting.views.view_category_product import CategoryProductViewSet
from sales_accounting.views.view_product import ProductViewSet
from sales_accounting.views.view_shop import ShopViewSet
from sales_accounting.views.view_warehose import WarehouseViewSet


router = SimpleRouter()
router.register('api/category', CategoryProductViewSet)
router.register('api/product', ProductViewSet)
router.register('api/warehouse', WarehouseViewSet)
router.register('api/shop', ShopViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
