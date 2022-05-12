from typing import List, Any
from asgiref.sync import sync_to_async
from backend.models import Doctor, Product, Order, Category


@sync_to_async
def get_doctor(password):
    try:
        user = Doctor.objects.filter(unique_password=password).first()
        return user
    except:
        return None


@sync_to_async
def get_product(kash):
    try:
        product = Product.objects.filter(kod=kash).first()
        return product
    except:
        return None


@sync_to_async
def add_order(product_kod, doctor):
    try:
        product = Product.objects.filter(kod=product_kod).first()
        doctor = Doctor.objects.filter(unique_password=doctor).first()
        return Order(product=product, doctor=doctor, count=1, summa=product.keshbek).save()
    except Exception as err:
        print(err)


@sync_to_async
def get_orders() -> List[Order]:
    try:
        users = Order.objects.all()
        return users
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def add_category(name):
    try:
        return Category(speciality=name).save()
    except Exception as err:
        print(err)


@sync_to_async
def add_product(product_name, category1, kod, keshbek):
    try:
        category = Category.objects.filter(speciality=category1).first()
        if not category:
            category = Category.objects.create(speciality=category1)
            category.save()
        return Product(product_name=product_name, category=category, kod=kod, keshbek=keshbek).save()
    except Exception as err:
        pass


@sync_to_async
def get_categories() -> List[Category]:
    try:
        users = Category.objects.all()
        return users
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def get_orders() -> List[Order]:
    try:
        users = Order.objects.all()
        return users
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def get_category_by_name(name):
    try:
        category = Category.objects.filter(speciality=name).first()
        return category
    except:
        return None


@sync_to_async
def get_order_by_product(name):
    try:
        orders = []
        products = Product.objects.filter(product_name=name)
        ords = Order.objects.all()
        for product in products:
            for order in ords:
                if order.product.product_name == product.product_name:
                    orders.append(order)
        return orders
    except:
        return None
