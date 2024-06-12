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


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE, verbose_name='Продукт', related_name='images')

    # def get_absolute_url(self, img=False):
    #     # current_img = self.image.url.split('/')[-1].split('.')[0]
    #     current_img = self.image.url.replace('/', '-').replace('.', '_')
    #
    #     return reverse('current_img', kwargs={
    #         'slug_cat': self.good.category.slug,
    #         'slug_good_name': self.good.slug,
    #         'current_img': current_img,
    #     })


class Categories(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.title

receiveMethod = [
    {'id': 1, 'name': "delivery_by_courier_in_Moscow"},
    {'id': 2, 'name': "delivery_by_sdek"},
    {'id': 3, 'name': "pickup"},
]


deliveryAddressMethods = [
    {'id': 1, 'name': "on_address"},
    {'id': 2, 'name': "on_metro"},
]


class Orders(models.Model):
    class OrderStatus(models.TextChoices):
        IN_PROCESSING = 'В обработке'
        NOT_PAID = 'Не оплачен'
        ACCEPTED = 'Принят',
        PAID = 'Оплачен',
        IN_DELIVERY_SERVICE = 'В службе доставки',
        DELIVERED = 'Доставлен',
        RECEIVED = 'Получен',

    class OrderReceiveMethod(models.TextChoices):
        DELIVERY_BY_COURIER_IN_MOSCOW = '1' , 'Доставка курьером по Москве'
        DELIVERY_BY_SDEK = '2' , 'Доставка СДЕКом'
        PICKUP = '3', 'Самовывоз'

    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    order_date = models.DateField(auto_now_add=True)
    delivery_address = models.CharField(max_length=50, verbose_name='Адрес доставки')
    receive_method = models.CharField(max_length=50, choices=OrderReceiveMethod.choices,
                                      default=OrderReceiveMethod.PICKUP, verbose_name='Способ получение')

    order_status = models.CharField(max_length=25, choices=OrderStatus.choices,
                                    default=OrderStatus.IN_PROCESSING, verbose_name='Статус заказа')
    delivey_cost = models.PositiveIntegerField(verbose_name='Стоимость доставки', default=0,)
    discount = models.PositiveIntegerField(verbose_name='Скидка', default=0,)
    final_cost = models.PositiveIntegerField(verbose_name='Итоговая стоимость', default=0,)
    products_cost = models.PositiveIntegerField(verbose_name='Цена всех товаров без скидки', default=0,)

    def __str__(self):
        return f"id-заказа: {self.id} user-id: {self.user.id}-{self.user.username}"



class OrderDetails(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Products', on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.title
