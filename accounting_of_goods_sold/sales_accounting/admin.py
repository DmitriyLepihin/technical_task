from django.contrib import admin

from sales_accounting.models import CategoryProduct, Product, Warehouse, Shop, SalesAccounting

admin.site.register(CategoryProduct)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Shop)
admin.site.register(SalesAccounting)
