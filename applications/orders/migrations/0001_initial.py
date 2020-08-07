# Generated by Django 3.0.5 on 2020-08-06 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0013_products_productcode'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Titulo')),
                ('resume', models.TextField(blank=True, verbose_name='Descripcion')),
                ('imagef', models.ImageField(upload_to='Product', verbose_name='Imagen Principal')),
                ('images', models.ImageField(blank=True, upload_to='Product', verbose_name='Imagen 2')),
                ('imaget', models.ImageField(blank=True, upload_to='Product', verbose_name='Imagen 3')),
                ('price', models.FloatField(verbose_name='Precio')),
                ('priceAnchor', models.FloatField(blank=True, null=True, verbose_name='Precio Anclaje')),
                ('pricePromo', models.FloatField(blank=True, null=True, verbose_name='Precio Promocion')),
                ('promotion', models.BooleanField(default=False, verbose_name='Promocion')),
                ('available', models.BooleanField(default=True, verbose_name='Disponible')),
                ('exhausted', models.BooleanField(default=False, verbose_name='Agotado')),
                ('season', models.BooleanField(default=False, verbose_name='Temporada')),
                ('virus', models.BooleanField(default=False, verbose_name='Virus')),
                ('calification', models.IntegerField(blank=True, default=0, verbose_name='Calificacion')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=1, verbose_name='Cantidad')),
                ('productCode', models.CharField(blank=True, max_length=100, verbose_name='Codigo de Producto')),
                ('colors', models.ManyToManyField(blank=True, to='product.Color')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Company')),
                ('sizes', models.ManyToManyField(blank=True, to='product.Size')),
                ('subCategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.SubCategory')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
