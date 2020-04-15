# Generated by Django 3.0.5 on 2020-04-15 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Categoria')),
                ('icono', models.ImageField(blank=True, upload_to='Category', verbose_name='Icono')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('address', models.CharField(blank=True, max_length=400, verbose_name='Direccion')),
                ('logo', models.ImageField(blank=True, upload_to='Company', verbose_name='Logo')),
                ('facebook', models.URLField(blank=True, verbose_name='Facebook')),
                ('twitter', models.URLField(blank=True, verbose_name='Twitter')),
                ('instagram', models.URLField(blank=True, verbose_name='Instagram')),
                ('youtube', models.URLField(blank=True, verbose_name='Youtube')),
                ('website', models.URLField(blank=True, verbose_name='WebSite')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-Mail')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='Telefono')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
                ('resume', models.TextField(blank=True, verbose_name='Resumen')),
                ('plan', models.BooleanField(default=False, verbose_name='Premium')),
                ('delivery', models.BooleanField(default=True, verbose_name='Nuestro Delivery')),
                ('phoneDelivery', models.CharField(blank=True, max_length=15, verbose_name='Telefono de Delivery')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Sub Categoria')),
                ('icono', models.ImageField(blank=True, upload_to='SubCategory', verbose_name='Icono')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Titulo')),
                ('resume', models.TextField(blank=True, verbose_name='Descripcion')),
                ('imagef', models.ImageField(blank=True, upload_to='Product', verbose_name='Imagen 1')),
                ('images', models.ImageField(blank=True, upload_to='Product', verbose_name='Imagen 2')),
                ('imaget', models.ImageField(blank=True, upload_to='Product', verbose_name='Imagen 3')),
                ('price', models.CharField(max_length=12, verbose_name='Precio')),
                ('priceAnchor', models.CharField(blank=True, max_length=12, verbose_name='Precio Anclaje')),
                ('pricePromo', models.CharField(blank=True, max_length=12, verbose_name='Precio Promocion')),
                ('promotion', models.BooleanField(default=False, verbose_name='Promocion')),
                ('available', models.BooleanField(default=True, verbose_name='Disponible')),
                ('calification', models.IntegerField(blank=True, default=0, verbose_name='Calificacion')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Company')),
                ('subCategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.SubCategory')),
            ],
        ),
    ]
