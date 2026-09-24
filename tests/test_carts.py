from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import CustomUser
from carts.models import Cart
from carts.api.serializers import CartSerializer
from carts.api.views import CartViewSet
from products.models import Product



class CreateViewCartsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create superuser
        self.superuser = CustomUser.objects.create_superuser(
            # username="Superuser Testing",
            first_name="Super",
            last_name="User",
            email="superuser@testing.com",
            password="superusertestingpassword",
        )
        self.superuser.save()
        # Create regular user
        self.user = CustomUser.objects.create_user(
            # username="Regular User",
            first_name="Regular",
            last_name="User",
            email="regularuser@testing.com",
            password="regularusertestingpassword",
        )
        self.user.save()
        # return super().setUp()()
    
    def test_not_authenticated_view_cart(self):
        """
        Tests whether non-authenticated user can 
        view their CART via GET/Retrieve request
        """
        response = self.client.get(path="/api/carts/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_retrives_their_cart(self):
        """
        Tests whether authenticated user only can 
        view their CART via GET/Retrieve request
        """
        self.client.login(
            email="regularuser@testing.com",
            password="regularusertestingpassword",
        )
        response = self.client.get(path=f"/api/carts/{self.user.cart.cartId}/")
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_only_retrives_their_cart(self):
        """
        Tests whether authenticated user only can 
        view their CART via GET/Retrieve request
        """
        self.client.login(email="regularuser@testing.com",password="regularusertestingpassword",)
        response = self.client.get(path=f"/api/carts/{self.superuser.cart.cartId}/")
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_update_cart_quantity(self):
        """
        Tests wheter an authenticated user can 
        update the quantity value of their cart
        """
        self.client.login(email="regularuser@testing.com",password="regularusertestingpassword",)
        response = self.client.patch(path=f"/api/carts/{self.user.cart.cartId}/",
                                     data={"quantity": 3},
                                     format="json",
                                     )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"],3)
    
    def test_authenticated_user_update_cart_product(self):
        """
        Tests wheter an authenticated user can 
        update the quantity value of their cart
        """
        self.client.login(email="regularuser@testing.com",password="regularusertestingpassword",)
        test_product = Product.objects.create(
            name="Test Product", slug="test-product", price="9.99"
        )        
        response = self.client.patch(path=f"/api/carts/{self.user.cart.cartId}/",
                                     data={"product": [test_product.pk]},
                                     format="json",
                                     )
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"],[test_product.pk])
    
    def test_authenticated_user_post_request(self):
        """
        Tests whether an authenticated user can
        make a POST request to /api/carts/ and 
        get the expected 405 Status
        """
        self.client.login(email="regularuser@testing.com",password="regularusertestingpassword",)
        response = self.client.post(path="/api/carts/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticated_user_delete_request(self):
        """
        Tests whether an authenticated user can
        make a DELETE request to /api/carts/ and 
        get the expected 405 Status
        """
        self.client.login(email="regularuser@testing.com",password="regularusertestingpassword",)
        response = self.client.delete(path="/api/carts/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    