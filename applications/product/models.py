from django.db import models
from django.utils.text import slugify 
from django.core.files.storage import FileSystemStorage
from django.conf import settings

image_storage = FileSystemStorage(
    location=u'{0}/'.format(settings.MEDIA_ROOT),
    base_url=u'{0}/'.format(settings.MEDIA_URL),
)

def company_image(instance, filename):
    return u'Company/{0}'.format(filename)

def category_image(instance, filename):
    return u'Category/{0}'.format(filename)

def subCategory_image(instance, filename):
    return u'SubCategory/{0}'.format(filename)

def product_image(instance, filename):
    return u'Products/{0}'.format(filename)


class Company(models.Model):
	name = models.CharField('Nombre', max_length=150, blank=False)
	address = models.CharField('Direccion', max_length=400, blank=True)
	logo = models.ImageField('Logo', upload_to=company_image, storage=image_storage, blank=True)
	facebook = models.URLField('Facebook', blank=True)
	twitter = models.URLField('Twitter', blank=True)
	instagram = models.URLField('Instagram', blank=True)
	youtube = models.URLField('Youtube', blank=True)
	website = models.URLField('WebSite', blank=True)
	email = models.EmailField('E-Mail', blank=True)
	phone = models.CharField('Telefono', max_length=15, blank=True)
	slug = models.SlugField('Slug', blank=True, unique=True)
	resume = models.TextField('Resumen', blank=True)
	delivery = models.BooleanField('Nuestro Delivery', default=True)
	phoneDelivery = models.CharField('Telefono de Delivery', max_length=15, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Company, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField('Categoria', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to=category_image, storage=image_storage, blank=True)
	slug = models.SlugField('Slug', blank=True, unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField('Sub Categoria', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to=subCategory_image, storage=image_storage, blank=True)
	category = models.ForeignKey(Category, models.SET_NULL, null=True)
	slug = models.SlugField('Slug', blank=True, unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(SubCategory, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Products(models.Model):
	title = models.CharField('Titulo', max_length=300, blank=False)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	subCategory = models.ForeignKey(SubCategory, models.SET_NULL, null=True)
	resume = models.TextField('Descripcion', blank=True)
	imagef = models.ImageField('Imagen 1', upload_to=product_image, storage=image_storage, blank=True)
	images = models.ImageField('Imagen 2', upload_to=product_image, storage=image_storage, blank=True)
	imaget = models.ImageField('Imagen 3', upload_to=product_image, storage=image_storage, blank=True)
	price = models.CharField('Precio', max_length=12, blank=False)
	available = models.BooleanField('Disponible', default=True)
	calification = models.IntegerField('Calificacion', blank=True, default=0)
	slug = models.SlugField('Slug', blank=True, unique=True)
	pub_date = models.DateField(auto_now=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Products, self).save(*args, **kwargs)

	def __str__(self):
		return self.title