from django.contrib import admin

from products.models import Cart
from .models import Users

# Register your models here.

class CartsInline(admin.TabularInline):
    model = Cart
    extra = 0

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username', )
    inlines = [CartsInline]
