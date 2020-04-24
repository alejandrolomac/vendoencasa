# Generated by Django 3.0.5 on 2020-04-24 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.TextField(blank=True, choices=[('Feminimo', 'Femenino'), ('Masculino', 'Masculino'), ('otro', 'otro')], max_length=500, null=True)),
                ('location', models.CharField(blank=True, max_length=400, null=True, verbose_name='Direccion')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefono')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
