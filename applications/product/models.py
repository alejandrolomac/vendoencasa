from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation

class Company(models.Model):
	name = models.CharField('Nombre', max_length=150, blank=False)
	address = models.CharField('Direccion', blank=True)
	logo = models.ImageField('Logo', upload_to='company/% Y/% m/% d/', blank=True)
	facebook = models.URLField('Facebook', blank=True)
	twitter = models.URLField('Twitter', blank=True)
	instagram = models.URLField('Instagram', blank=True)
	youtube = models.URLField('Youtube', blank=True)
	website = models.URLField('WebSite', blank=True)
	email = models.EmailField('E-Mail', blank=True)
	phone = models.CharField('Telefono', blank=True)
	slug = models.SlugField('Slug', blank=False, unique=True)
	resume = models.TextField('Resumen', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField('Nombre', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to='category/% Y/% m/% d/', blank=True)
	slug = models.SlugField('Slug', blank=False, unique=True)

	def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
    	return self.name


class SubCategory(models.Model):
	name = models.CharField('Nombre', max_length=100, unique=False)
	icono = models.ImageField('Icono', upload_to='subcategory/% Y/% m/% d/', blank=True)
	category = models.ForeignKey(Category)
	slug = models.SlugField('Slug', blank=False, unique=True)

	def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
    	return self.name


class Product(models.Model):
	title = models.CharField('Titulo', blank=False)
	company = models.ForeignKey('Empresa', Company, on_delete=models.CASCADE)
	category = GenericRelation('Categoria', Category)
	subCategory = GenericRelation('Sub Categoria', SubCategory)
	resume = models.TextField('Descripcion', blank=True)
	imagef = models.ImageField('Imagen 1', upload_to='company/% Y/% m/% d/', blank=True)
	images = models.ImageField('Imagen 2', upload_to='company/% Y/% m/% d/', blank=True)
	imaget = models.ImageField('Imagen 3', upload_to='company/% Y/% m/% d/', blank=True)
	price = models.CharField('Precio', blank=False)
	calification = models.IntegerField('Calificacion', blank=True)
	slug = models.SlugField('Slug', blank=False, unique=True)

	def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

	def __str__(self):
		return self.title