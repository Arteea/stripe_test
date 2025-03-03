from django.db import models

### Список доступных валют
currency_list = [('usd','usd'),('eur','eur'),('rub','rub')]

class Item(models.Model):
    
    '''
    Модель товара, представляющая отдельный товар.
    Содержит информацию o названии, описании, валюте и цене товара.
    '''

    name = models.CharField(max_length=150, unique=True, verbose_name= "Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price  = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=3,choices = currency_list, default = 'usd', verbose_name='Валюта')

    
    class Meta:

        verbose_name = "Товар"
        verbose_name_plural = 'Товары'


    def __str__(self):

        return f'Цена за {self.name} - {self.price}'



class Discount(models.Model):

    name = models.CharField(max_length=150, unique=True, verbose_name= "Название скидки")
    percentage = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='Процент скидки')

    class Meta:

        verbose_name = "Скидка"
        verbose_name_plural = 'Скидки'

    def __str__(self):

        return f"Скидка {self.name}  - {self.percentage}%"


class Tax(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name= "Название налога")
    percentage = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='Процент налога')

    class Meta:

        verbose_name = "Налог"
        verbose_name_plural = 'Налоги'

    def __str__(self):

        return f"Налог {self.name}  - {self.percentage}%"
    



class Order(models.Model):
    items = models.ManyToManyField(to=Item,through='OrderItem', verbose_name='Товары')
    discount = models.ManyToManyField(to=Discount, blank=True, verbose_name="Скидка")
    tax = models.ForeignKey(to=Tax, default=1, null=True, blank=True,on_delete=models.SET_NULL, verbose_name="Налог")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:

        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'
        
        
    def calculate_full_price(self):
        
        total_price = sum(it.item.price * it.quantity for it in self.order_items.all())
    
        return total_price



class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items")
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

