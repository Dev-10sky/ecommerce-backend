from rest_framework import viewsets,mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from carts.models import Cart
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer





class CartViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin
                  ,viewsets.GenericViewSet):
    serializer_class = CartSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["cartId", "name"]
    permission_classes = [IsAuthenticated]
    lookup_field  = "cartId"

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)