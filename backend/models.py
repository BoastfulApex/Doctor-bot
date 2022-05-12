from django.db import models


class Category(models.Model):
    speciality = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.speciality


class Doctor(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    unique_password = models.CharField(max_length=9, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    kod = models.CharField(max_length=10, unique=True)
    keshbek = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    summa = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name
