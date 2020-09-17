from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify 
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse

GENDER_CHOICES = (
    ('Femenino','Femenino'),
    ('Masculino', 'Masculino'),
    ('Otro','Otro'),
)

PLAN_CHOICES = (
    ('Comprador','Comprador'),
    ('Vendedor','Vendedor'),
    ('Empresario', 'Empresario'),
    ('Franquiciador','Franquiciador'),
)

DEPARTMENT_CHOICES = (
    ('Atlántida','Atlántida'),
    ('Colón','Colón'),
    ('Comayagua','Comayagua'),
    ('Copán','Copán'),
    ('Cortés','Cortés'),
    ('Choluteca','Choluteca'),
    ('El Paraíso','El Paraíso'),
    ('Francisco Morazán','Francisco Morazán'),
    ('Gracias a Dios','Gracias a Dios'),
    ('Intibucá','Intibucá'),
    ('Islas de la Bahía','Islas de la Bahía'),
    ('La Paz','La Paz'),
    ('Lempira','Lempira'),
    ('Ocotepeque','Ocotepeque'),
    ('Olancho','Olancho'),
    ('Santa Bárbara','Santa Bárbara'),
    ('Valle','Valle'),
    ('Yoro','Yoro'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    gender = models.TextField('Genero', max_length=500, choices=GENDER_CHOICES, blank=True, null=True)
    Department = models.CharField('Departamento #1', max_length=500, blank=True, null=True, choices=DEPARTMENT_CHOICES, default='Francisco Morazán')
    location = models.CharField('Dirección Detallada #1', max_length=500, blank=True, null=True)
    Departments = models.CharField('Departamento #2', max_length=500, blank=True, null=True, choices=DEPARTMENT_CHOICES, default='Francisco Morazán')
    locations = models.CharField('Dirección Detallada #2', max_length=500, blank=True, null=True)
    Departmentt = models.CharField('Departamento #3', max_length=500, blank=True, null=True, choices=DEPARTMENT_CHOICES, default='Francisco Morazán')
    locationt = models.CharField('Dirección Detallada #3', max_length=500, blank=True, null=True)
    phone = models.CharField('Teléfono', max_length=15, blank=True, null=True)
    name = models.CharField('Nombre Empresa', max_length=150, blank=True)
    logo = models.ImageField('Logo', upload_to='Company', blank=True)
    facebook = models.URLField('Facebook', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    website = models.URLField('Sitio Web', blank=True)
    resume = models.TextField('Descripción Empresa', blank=True)
    plan = models.TextField('Plan', max_length=50, choices=PLAN_CHOICES, blank=True, default='Comprador')
    points = models.IntegerField('Puntos', default=0, blank=True, null=True )
    slug = models.SlugField('Slug', blank=True, unique=True)
    code = models.CharField("Codigo de Registro", max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if( self.name ):
            self.slug = slugify(self.name)
            super(Profile, self).save(*args, **kwargs)
        else:
            self.slug = slugify(self.user.username)
            super(Profile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()