from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from carts.models import Cart


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager with email as the unique identifier
    """

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Create user with the given email and password.
        """
        if not email:
            raise ValueError("The email must be set")
        first_name = first_name.capitalize()
        last_name = last_name.capitalize()
        email = self.normalize_email(email)

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """
        Create superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(first_name, last_name, email, password, **extra_fields)

# Created CustomUserCartManager Class
class CustomUserCartManager(models.Manager):

    def create_cart(self,user):
        cart = self.create(user=user)
        cart.save()
        return cart
    
class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, verbose_name="First name")
    last_name = models.CharField(max_length=255, verbose_name="Last name")
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
# Signal code to create Cart attached to user
@receiver(post_save,sender=CustomUser)
def cart_create(sender, instance, created=False, **kwargs):
    if created:
        print(instance.first_name)
        carts_name = str(instance.first_name)+ " " +str(instance.last_name)+ "'s " + "Cart" 
        newCart = Cart.objects.create(user=instance,name=carts_name)
        newCart.save()