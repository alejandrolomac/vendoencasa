from django.db import models
from django.utils.text import slugify 
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

PLAN_CHOICES = (
    ('Vendedor','Vendedor'),
    ('Empresario', 'Empresario'),
    ('Franquiciador','Franquiciador'),
)

CALIFICATION_CHOICES = (
    ('1','1'),
    ('2', '2'),
    ('3','3'),
	('4','4'),
	('5','5'),
)


class Company(models.Model):
	name = models.CharField('Nombre', max_length=150, blank=False)
	address = models.CharField('Direccion', max_length=400, blank=True)
	logo = models.ImageField('Logo', upload_to='Company', blank=True)
	facebook = models.URLField('Facebook', blank=True)
	twitter = models.URLField('Twitter', blank=True)
	instagram = models.URLField('Instagram', blank=True)
	youtube = models.URLField('Youtube', blank=True)
	website = models.URLField('WebSite', blank=True)
	email = models.EmailField('E-Mail', blank=True)
	phone = models.CharField('Telefono', max_length=15, blank=True)
	slug = models.SlugField('Slug', blank=True, unique=True)
	resume = models.TextField('Resumen', blank=True)
	plan = models.TextField('Plan', max_length=50, choices=PLAN_CHOICES, blank=True, default='Vendedor')
	delivery = models.BooleanField('Nuestro Delivery', default=True)
	phoneDelivery = models.CharField('Telefono de Delivery', max_length=15, blank=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Company, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField('Categoria', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to='Category', blank=True)
	categoryCode = models.CharField('Codigo Categoría', max_length=1, blank=True)
	slug = models.SlugField('Slug', blank=True, unique=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField('Sub Categoria', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to='SubCategory', blank=True)
	category = models.ForeignKey(Category, models.SET_NULL, null=True)
	slug = models.SlugField('Slug', blank=True, unique=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(SubCategory, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Color(models.Model):
	name = models.CharField('Nombre', max_length=100)
	color = models.CharField('Color', max_length=10)

	def __str__(self):
		return self.name

class Size(models.Model):
	name = models.CharField('Talla', max_length=100)

	def __str__(self):
		return self.name

class Products(models.Model):
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
	quantity = models.IntegerField('Cantidad', default=1, blank=False)
	productCode = models.CharField("Codigo de Producto", max_length=100, blank=True)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		origin_slug = slugify(self.title)
		unique_slug = origin_slug
		numb = 1
		while Products.objects.filter(slug=unique_slug).exists():
			unique_slug = '%s-%d' % (origin_slug, numb)
			numb += 1
		self.slug = unique_slug
		super(Products, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("product_app:product", kwargs={"slug": self.slug})
	
	def get_add_to_cart_url(self):
		return reverse("cart_app:add-to-cart", kwargs={"slug": self.slug})

	def get_add_to_cart_from_wish_url(self):
		return reverse("cart_app:add-to-cart-from-wish", kwargs={"slug": self.slug})

	def get_add_to_wish_url(self):
		return reverse("wish_app:add_to_whis", kwargs={"slug": self.slug})
	
	def get_remove_from_wish_url(self):
		return reverse("wish_app:remove-to-whis", kwargs={"slug": self.slug})

	def get_remove_from_cart_url(self):
		return reverse("cart_app:remove-to-cart", kwargs={"slug": self.slug})
	
	def offer_save(self):
		if self.priceAnchor:
			savedt = self.priceAnchor - self.pricePromo 
		else:
			savedt = self.price - self.pricePromo 
		
		offer_total = (savedt * 100) / self.price
		return offer_total

@receiver(post_save, sender=Products)
def save_code(sender, instance, **kwargs):
	catCode = instance.subCategory.category.categoryCode + str(instance.subCategory.id).zfill(2)
	proCode = str(instance.id)
	if instance.company:
		compaCode = str(instance.company.id)
	else:
		compaCode = str(instance.user.id)

	codeFinal = str(catCode + '-' + proCode + '-' + compaCode)
	if instance.productCode != codeFinal:
		instance.productCode = codeFinal
		instance.save()

class Comment(models.Model):
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)
	comment = models.TextField('Comentario', blank=True)
	calification = models.TextField('Calificacion', blank=True, default=1, choices=CALIFICATION_CHOICES)
	imagef = models.ImageField('Imagen 1', upload_to='Comment', blank=True)
	images = models.ImageField('Imagen 2', upload_to='Comment', blank=True)
	imaget = models.ImageField('Imagen 3', upload_to='Comment', blank=True)
	pub_date = models.DateTimeField(editable=False, auto_now=True)

	def __str__(self):
		return self.comment