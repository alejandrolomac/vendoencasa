from django.db import models
from django.utils.text import slugify 

class Company(models.Model):
	name = models.CharField('Nombre', max_length=150, blank=False)
	address = models.CharField('Direccion', max_length=400, blank=True)
	logo = models.ImageField('Logo', upload_to='company/% Y/% m/% d/', blank=True)
	facebook = models.URLField('Facebook', blank=True)
	twitter = models.URLField('Twitter', blank=True)
	instagram = models.URLField('Instagram', blank=True)
	youtube = models.URLField('Youtube', blank=True)
	website = models.URLField('WebSite', blank=True)
	email = models.EmailField('E-Mail', blank=True)
	phone = models.CharField('Telefono', max_length=15, blank=True)
	slug = models.SlugField('Slug', blank=True, unique=True)
	resume = models.TextField('Resumen', blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Company, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField('Categoria', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to='category/% Y/% m/% d/', blank=True)
	slug = models.SlugField('Slug', blank=True, unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField('Sub Categoria', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to='subcategory/% Y/% m/% d/', blank=True)
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
	imagef = models.ImageField('Imagen 1', upload_to='company/% Y/% m/% d/', blank=True)
	images = models.ImageField('Imagen 2', upload_to='company/% Y/% m/% d/', blank=True)
	imaget = models.ImageField('Imagen 3', upload_to='company/% Y/% m/% d/', blank=True)
	price = models.CharField('Precio', max_length=12, blank=False)
	calification = models.IntegerField('Calificacion', blank=True, default=0)
	slug = models.SlugField('Slug', blank=True, unique=True)
	pub_date = models.DateField(auto_now=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Products, self).save(*args, **kwargs)

	def __str__(self):
		return self.title