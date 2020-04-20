from django.conf import settings
from django.db import models
from applications.product.models import Products

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} de {self.item.title}"
    
    def get_total_item_price(self):
        precio_total = self.quantity * self.item.price
        return precio_total

    def get_total_discount_item_price(self):
        precio_descuento_total = self.quantity * self.item.pricePromo
        return precio_descuento_total
    
    def get_amount_saved(self):
        saved_total = self.get_total_item_price() - self.get_total_discount_item_price()
        return saved_total

    def get_final_price(self):
        if self.item.pricePromo:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def stringNames(self):
        text = ''
        for name in self.items.all():
            text += '- ' + name.item.title + ' > ' + name.item.company.name + '%0D%0A'
        return text