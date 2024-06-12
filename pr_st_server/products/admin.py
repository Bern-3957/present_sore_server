from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Products, Categories, Orders, OrderDetails, Cart, Gallery


# Register your models here.


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    fields = ("get_product_id", "get_product_title", 'get_html_image',)
    readonly_fields = ("get_product_id", "get_product_title", 'get_html_image',)

    def get_product_id(self, obj):
        return obj.product.id
    get_product_id.short_description = "ID продукта"
    def get_product_title(self, obj):
        return obj.product.title
    get_product_title.short_description = "Название продукта"

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=70>")

    get_html_image.short_description = "Картинка"

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 0

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "is_published", "created_at",)
    list_display_links = ("id", "title", )
    inlines = [GalleryInline]


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 0

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "order_date",
                    "user_id",
                    "get_username",
                    "order_date",
                    "order_status",
                    "delivery_address",
                    "receive_method",
                    "delivey_cost",
                    "discount",
                    "final_cost")

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "Username"
    get_username.admin_order_field = 'username'
    list_display_links = ("id","get_username",)
    inlines = [OrderDetailsInline]


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    fields = ("__all__",)
    # list_display_links = ("id", )




admin.site.register(Cart)
