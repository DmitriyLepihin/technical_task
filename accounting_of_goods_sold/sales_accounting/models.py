from django.db import models


class CategoryProduct(models.Model):
    name_category = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.name_category}"

    class Meta:
        verbose_name = 'Category Product'
        verbose_name_plural = 'Category Products'


class Product(models.Model):
    name_product = models.CharField(max_length=300)
    category_product_id = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name_product}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Warehouse(models.Model):
    name_warehouse = models.CharField(max_length=300)
    products = models.ManyToManyField(Product)
    receipt_date = models.DateField()
    count_product = models.IntegerField()

    def __str__(self):
        return f"{self.name_warehouse}"

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['receipt_date']


class Shop(models.Model):
    name_shop = models.CharField(max_length=400)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_product = models.FloatField()
    warehouses = models.ManyToManyField(Warehouse)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.name_shop}"

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class SalesAccounting(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouses_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    category_product_id = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sales Accounting'
        verbose_name_plural = 'Sales Accounting'
