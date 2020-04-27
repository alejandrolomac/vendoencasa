from django.db import models
from django.utils.text import slugify 
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse

class Services(models.Model):
    name = models.CharField('Nombre', max_length=150, blank=False)
    address = models.CharField('Direccion', max_length=400, blank=True)
    logo = models.ImageField('Logo', upload_to='Services', blank=True)
    facebook = models.URLField('Facebook', blank=True)
    twitter = models.URLField('Twitter', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    youtube = models.URLField('Youtube', blank=True)
    website = models.URLField('WebSite', blank=True)
    email = models.EmailField('E-Mail', blank=True)
    phone = models.CharField('Telefono', max_length=15, blank=True)
    slug = models.SlugField('Slug', blank=True, unique=True)
    resume = models.TextField('Resumen', blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Services, self).save(*args, **kwargs)

    def __str__(self):
        return self.name