from django.conf import settings
from django.db import models
from applications.product.models import Products, DiscountCode

STATUS_CHOICES = (
    ('NoPagados','NoPagados'),
    ('Procesando', 'Procesando'),
    ('Enviado','Enviado'),
    ('Pagado','Pagado'),
    ('Comentado', 'Comentado'),
    ('Devuelto', 'Devuelto'),
)

PAYSTATUS_CHOICES = (
    ('NoPagados','NoPagados'),
    ('Procesando', 'Procesando'),
    ('Pagado','Pagado'),
)

PAYMETHOD_CHOICES = (
    ('Efectivo','Efectivo'),
    ('Tarjeta', 'Tarjeta'),
    ('PayPal','PayPal'),
	('Link', 'Link'),
	('Deposito', 'Deposito'),
)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    orderItemCode = models.CharField("Codigo de Item", max_length=100, blank=True)

    def __str__(self):
        if self.orderItemCode:
            return f"{self.quantity} de {self.item.title}: {self.color} Talla: {self.size} Codigo: {self.orderItemCode}"
        else:
            return f"{self.quantity} de {self.item.title}: {self.color} Talla: {self.size}"

    def save(self, *args, **kwargs):
        self.orderItemCode =  str(self.item.productCode)
        super(OrderItem, self).save(*args, **kwargs)
    
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
    discountCode = models.CharField("Codigo de Descuento", max_length=100, blank=True)
    orderCode = models.CharField("Codigo de Pedido", max_length=300, blank=True)
    status = models.TextField('Estado', max_length=50, choices=STATUS_CHOICES, blank=True, default='NoPagados')
    orderLocation = models.CharField('Dirección de Envío', max_length=500, blank=True, null=True)
    payMethod = models.CharField('Metodo de Pago', max_length=500, blank=True, null=True, choices=PAYMETHOD_CHOICES, default='Efectivo')
    paystaus = models.TextField('Estado de Pago', max_length=50, choices=PAYSTATUS_CHOICES, blank=True, default='NoPagados')
    
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.orderCode =  str(self.id) + '-' + str(self.user.id) + '-' + str(self.ordered_date.strftime('%Y%m%d'))
        super(Order, self).save(*args, **kwargs)
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    
    def get_price_envio(self):
        envio = 0
        for order_item in self.items.all():
            envio += 1
        envio = (envio - 1) * 20 + 80
        return envio
    
    def get_discount(self):
        if self.discountCode:
            discode = DiscountCode.objects.get(code=self.discountCode)
            if discode.typediscount == 'Fijo':
                descuentototal = discode.discount
            else:
                descuentototal = discode.discount
                descuentototal = self.get_total() * discode.discount / 100
        else:
            descuentototal = 0
        return descuentototal

    
    def get_total_final(self):
        total = 0
        envio = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
            envio += 1
        envio = (envio - 1) * 20 + 80
        totalf = total + envio
        return totalf

    def stringNames(self):
        text = ''
        for name in self.items.all():
            if( not name.item.company ):
                text += '- ' + str(name.item.title) + ': ' + str(name.get_color()) + str(name.get_size()) + str(name.get_quantity()) + ' > ' + str(name.item.user.profile.name) + '%0D%0A'
            else:
                text += '- ' + str(name.item.title) + ': ' + str(name.get_color()) + str(name.get_size()) + str(name.get_quantity()) + ' > ' + str(name.item.company.name) + '%0D%0A'
        return text