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
    ('Vendedor','Vendedor'),
    ('Empresario', 'Empresario'),
    ('Franquiciador','Franquiciador'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    gender = models.TextField('Genero', max_length=500, choices=GENDER_CHOICES, blank=True, null=True)
    location = models.CharField('Dirección', max_length=400, blank=True, null=True)
    phone = models.CharField('Teléfono', max_length=15, blank=True, null=True)
    name = models.CharField('Nombre Empresa', max_length=150, blank=True)
    logo = models.ImageField('Logo', upload_to='Company', blank=True)
    facebook = models.URLField('Facebook', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    website = models.URLField('Sitio Web', blank=True)
    resume = models.TextField('Descripción Empresa', blank=True)
    plan = models.TextField('Plan', max_length=50, choices=PLAN_CHOICES, blank=True, default='Vendedor')
    points = models.IntegerField('Puntos', default=0, blank=True, null=True )
    slug = models.SlugField('Slug', blank=True, unique=True)

    def save(self, *args, **kwargs):
        if( self.name ):
            self.slug = slugify(self.name)
            super(Profile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()