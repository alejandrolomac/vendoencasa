from django.conf import settings
from django.db import models
from applications.product.models import Products

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} de {self.item.title}: {self.color} Talla: {self.size}"
    
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

    def get_color(self):
        if self.color:
            colortext = ' -Color: ' + str(self.color) + '- ' 
        else:
            colortext = ''
        return colortext
    
    def get_size(self):
        if self.size:
            sizetext = ' -Talla: ' + str(self.size) + '- ' 
        else:
            sizetext = ''
        return sizetext

    def get_quantity(self):
        quantitytext = self.quantity
        return quantitytext

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
            if( not name.item.company ):
                text += '- ' + str(name.item.title) + ': ' + str(name.get_color()) + str(name.get_size()) + str(name.get_quantity()) + ' > ' + str(name.item.user.profile.name) + '%0D%0A'
            else:
                text += '- ' + str(name.item.title) + ': ' + str(name.get_color()) + str(name.get_size()) + str(name.get_quantity()) + ' > ' + str(name.item.company.name) + '%0D%0A'
        return text