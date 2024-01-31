from django.db import models
from users.models import Users

# export const purposes = [
#     {id: 'pur-123', title: 'Для кухни'},
#     {id: 'pur-234', title: 'Для бани'},
#     {id: 'pur-345', title: 'В гости'},
#     {id: 'pur-456', title: 'Косметические наборы'},
# ];
# Create your models here.
purposes = (
    ('FOR_KITCHEN', 'Для кухни'),
    ('FOR_BATHROOM', 'Для бани'),
    ('VISITING', 'В гости'),
    ('COSMETIC_KITS', 'Косметические наборы'),
    (None, 'Без назначения'),
)
packages = (
    ('BASKET', 'Корзина'),
    ('BOX', 'Коробка'),
    ('PACKAGE', 'Пакет'),
    ('CASE', 'Ящик'),
    (None, 'Без упаковки'),

)


class Products(models.Model):
    category = models.ForeignKey('Categories', on_delete=models.PROTECT, verbose_name='Категория')
    title = models.CharField(max_length=300, verbose_name='Наименование товара')
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edible = models.BooleanField(default=False)
    purpose = models.CharField(max_length=47, choices=purposes, verbose_name='Назначение', null=True, blank=True)
    package = models.CharField(max_length=47, choices=packages, verbose_name='Упаковка', null=True, blank=True)
    vendor_code = models.IntegerField(unique=True, verbose_name='Артикул')
    quantity_in_stock = models.IntegerField(default=0, verbose_name='Количество на складе')

    def __str__(self):
        return self.title


class Categories(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.title

    
class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    order_date = models.DateField(auto_now_add=True)


class OrderDetails(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Products', on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
