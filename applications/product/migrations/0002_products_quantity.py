# Generated by Django 3.0.5 on 2020-04-17 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
