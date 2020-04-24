from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
    ('Feminimo','Femenino'),
    ('Masculino', 'Masculino'),
    ('otro','otro'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    gender = models.TextField(max_length=500, choices=GENDER_CHOICES, blank=True, null=True)
    location = models.CharField('Direccion', max_length=400, blank=True, null=True)
    phone = models.CharField('Telefono', max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()