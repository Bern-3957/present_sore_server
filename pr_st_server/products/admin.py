from django.contrib import admin
from .models import Products, Categories, Orders, OrderDetails, Cart


# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Categories, CategoryAdmin)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(OrderDetails)
admin.site.register(Cart)
