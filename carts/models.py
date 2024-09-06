from django.db import models
from django.urls import reverse
from products.models import Product
from src.settings.base import *



class Cart(models.Model):
    cartId = models.AutoField(primary_key=True)
    product = models.ManyToManyField(Product, blank=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    quantity = models.IntegerField(default=0) # number of items in cart
    user = models.OneToOneField(AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        ordering = ("name",)
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return self.name
    
    @property
    def is_empty(self):
        return self.quantity == 0
