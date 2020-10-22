# Generated by Django 3.0.5 on 2020-10-21 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, max_length=50)),
                ('size', models.CharField(blank=True, max_length=50)),
                ('ordered', models.BooleanField(default=False)),
                ('wishItemCode', models.CharField(blank=True, max_length=100, verbose_name='Codigo de Item Deseado')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('orderCode', models.CharField(blank=True, max_length=300, verbose_name='Codigo de Deseo')),
                ('items', models.ManyToManyField(to='wish.WishItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
