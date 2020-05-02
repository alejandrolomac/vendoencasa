# Generated by Django 3.0.5 on 2020-05-02 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20200424_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Talla')),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='product.Size'),
        ),
    ]
