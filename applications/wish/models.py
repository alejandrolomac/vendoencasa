from django.conf import settings
from django.db import models
from applications.product.models import Products

class WishItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    ordered = models.BooleanField(default=False)
    wishItemCode = models.CharField("Codigo de Item Deseado", max_length=100, blank=True)

    def __str__(self):
        if self.wishItemCode:
            return f"{self.item.title}: {self.color} Talla: {self.size} Codigo: {self.wishItemCode}"
        else:
            return f"{self.item.title}: {self.color} Talla: {self.size}"

    def save(self, *args, **kwargs):
        self.wishItemCode =  str(self.item.productCode)
        super(WishItem, self).save(*args, **kwargs)

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

class Wish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(WishItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    orderCode = models.CharField("Codigo de Deseo", max_length=300, blank=True)
    
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.orderCode =  str(self.id) + '-' + str(self.user.id) + '-' + str(self.ordered_date.strftime('%Y%m%d'))
        super(Wish, self).save(*args, **kwargs)

    def stringNames(self):
        text = ''
        for name in self.items.all():
            if( not name.item.company ):
                text += '- ' + str(name.item.title) + ': ' + str(name.get_color()) + str(name.get_size()) + ' > ' + str(name.item.user.profile.name) + '%0D%0A'
            else:
                text += '- ' + str(name.item.title) + ': ' + str(name.get_color()) + str(name.get_size()) + ' > ' + str(name.item.company.name) + '%0D%0A'
        return text