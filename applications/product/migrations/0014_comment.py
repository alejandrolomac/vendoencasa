# Generated by Django 3.0.5 on 2020-08-21 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_products_productcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, verbose_name='Comentario')),
                ('calification', models.IntegerField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default=1, verbose_name='Calificacion')),
                ('imagef', models.ImageField(blank=True, upload_to='Comment', verbose_name='Imagen 1')),
                ('images', models.ImageField(blank=True, upload_to='Comment', verbose_name='Imagen 2')),
                ('imaget', models.ImageField(blank=True, upload_to='Comment', verbose_name='Imagen 3')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Products')),
            ],
        ),
    ]
