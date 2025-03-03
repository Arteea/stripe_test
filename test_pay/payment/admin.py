from django.contrib import admin

from payment.models import Item,Order,Discount,Tax,OrderItem


admin.site.register(Item)
admin.site.register(Discount)
admin.site.register(Tax)
admin.site.register(OrderItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_items', 'is_paid', 'tax', 'get_discount']

    def get_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])

    def get_discount(self, obj):
        return ", ".join([discount.name for discount in obj.discount.all()])

    get_items.short_description = "Items"
    get_discount.short_description = "Discounts"