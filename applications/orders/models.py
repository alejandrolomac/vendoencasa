from django.db import models
from django.utils.text import slugify 
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from applications.product.models import Color, Size, SubCategory, Category, Company

class OrdersProducts(models.Model):
	title = models.CharField('Titulo', max_length=300, blank=False)
	company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
	subCategory = models.ForeignKey(SubCategory, models.SET_NULL, null=True)
	resume = models.TextField('Descripcion', blank=True)
	imagef = models.ImageField('Imagen Principal', upload_to='Product', null=False)
	images = models.ImageField('Imagen 2', upload_to='Product', blank=True)
	imaget = models.ImageField('Imagen 3', upload_to='Product', blank=True)
	price = models.FloatField('Precio', blank=False)
	priceAnchor = models.FloatField('Precio Anclaje', blank=True, null=True)
	pricePromo = models.FloatField('Precio Promocion', blank=True, null=True)
	promotion = models.BooleanField('Promocion', default=False)
	available = models.BooleanField('Disponible', default=True)
	exhausted = models.BooleanField('Agotado', default=False)
	season = models.BooleanField('Temporada', default=False)
	virus = models.BooleanField('Virus', default=False)
	colors = models.ManyToManyField(Color, blank=True)
	sizes = models.ManyToManyField(Size, blank=True)
	calification = models.IntegerField('Calificacion', blank=True, default=0)
	slug = models.SlugField('Slug', blank=True, unique=True)
	pub_date = models.DateTimeField(editable=False, auto_now=True)
	quantity = models.IntegerField('Cantidad', default=1)
	productCode = models.CharField("Codigo de Producto", max_length=100, blank=True)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		catCode = self.subCategory.category.categoryCode + str(self.subCategory.id).zfill(2)
		proCode = str(self.id)
		if self.company:
			compaCode = str(self.company.id)
		else:
			compaCode = str(self.user.id)
		self.slug = slugify(self.title)
		self.productCode = catCode + '-' + proCode + '-' + compaCode
		super(OrdersProducts, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("product_app:product", kwargs={"slug": self.slug})
	
	def get_add_to_cart_url(self):
		return reverse("orders_app:single-orders", kwargs={"slug": self.slug})

	def get_remove_from_cart_url(self):
		return reverse("cart_app:remove-to-cart", kwargs={"slug": self.slug})
	
	def offer_save(self):
		if self.priceAnchor:
			savedt = self.priceAnchor - self.pricePromo 
		else:
			savedt = self.price - self.pricePromo 
		
		offer_total = (savedt * 100) / self.price
		return offer_total

	def total_price(self):
		if self.pricePromo:
			total = self.pricePromo 
		else:
			total = self.price
		
		totalPrice = total
		return totalPrice