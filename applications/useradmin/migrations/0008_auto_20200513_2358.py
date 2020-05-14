# Generated by Django 3.0.5 on 2020-05-14 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useradmin', '0007_auto_20200513_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='plan',
            field=models.BooleanField(blank=True, choices=[('Vendedor', 'Vendedor'), ('Empresario', 'Empresario'), ('Franquiciador', 'Franquiciador')], default='Vendedor', max_length=50, verbose_name='Plan'),
        ),
    ]
