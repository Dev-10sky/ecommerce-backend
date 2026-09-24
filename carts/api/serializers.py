from rest_framework import serializers
from products.models import Category, Product
from carts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            "cartId",
            "product",
            "name",
            "quantity",
            "slug",
        )
