from django.contrib import admin
from carts.models import Cart



class CartAdmin(admin.ModelAdmin):
    list_display = ("name","quantity",)
    list_filter = ("name","quantity",)
    list_editable = ("quantity",)

    # Shopping Cart name as slug value
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Cart,CartAdmin)
