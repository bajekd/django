from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=32, null=True)
    email = models.CharField(max_length=75, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ("Indoor", "Indoor"), # (what goes to db, what will be display) 
        ("Outdoor", "Outdoor"),
    )

    name = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out of delivery", "Out of delivery"),
        ("Delivered", "Delivered"),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL) #if your fk model is in above this line, just type name like here / if your fk 
    #model is below this line you have 2 options: 1) rearrange file 2) type "NAME_OF_YOUR_FK_MODEL" - here it would be "Customer" ("" tells django that model is in
    #this file) 
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateField(auto_now_add=True, null=True)
    note = models.CharField(max_length=125, null=True)

    def __str__(self):
        return self.product.name
