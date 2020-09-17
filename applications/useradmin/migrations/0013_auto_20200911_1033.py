# Generated by Django 3.0.5 on 2020-09-11 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useradmin', '0012_auto_20200905_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Department',
            field=models.CharField(blank=True, choices=[('Atlantida', 'Atlántida'), ('Colon', 'Colón'), ('Comayagua', 'Comayagua'), ('Copan', 'Copán'), ('Cortes', 'Cortés'), ('Choluteca', 'Choluteca'), ('ElParaiso', 'El Paraíso'), ('FranciscoMorazan', 'Francisco Morazán'), ('GraciasaDios', 'Gracias a Dios'), ('Intibuca', 'Intibucá'), ('IslasdelaBahia', 'Islas de la Bahía'), ('LaPaz', 'La Paz'), ('Lempira', 'Lempira'), ('Ocotepeque', 'Ocotepeque'), ('Olancho', 'Olancho'), ('SantaBarbara', 'Santa Bárbara'), ('Valle', 'Valle'), ('Yoro', 'Yoro')], default='FranciscoMorazan', max_length=500, null=True, verbose_name='Departamento #1'),
        ),
        migrations.AddField(
            model_name='profile',
            name='Departments',
            field=models.CharField(blank=True, choices=[('Atlantida', 'Atlántida'), ('Colon', 'Colón'), ('Comayagua', 'Comayagua'), ('Copan', 'Copán'), ('Cortes', 'Cortés'), ('Choluteca', 'Choluteca'), ('ElParaiso', 'El Paraíso'), ('FranciscoMorazan', 'Francisco Morazán'), ('GraciasaDios', 'Gracias a Dios'), ('Intibuca', 'Intibucá'), ('IslasdelaBahia', 'Islas de la Bahía'), ('LaPaz', 'La Paz'), ('Lempira', 'Lempira'), ('Ocotepeque', 'Ocotepeque'), ('Olancho', 'Olancho'), ('SantaBarbara', 'Santa Bárbara'), ('Valle', 'Valle'), ('Yoro', 'Yoro')], default='FranciscoMorazan', max_length=500, null=True, verbose_name='Departamento #2'),
        ),
        migrations.AddField(
            model_name='profile',
            name='Departmentt',
            field=models.CharField(blank=True, choices=[('Atlantida', 'Atlántida'), ('Colon', 'Colón'), ('Comayagua', 'Comayagua'), ('Copan', 'Copán'), ('Cortes', 'Cortés'), ('Choluteca', 'Choluteca'), ('ElParaiso', 'El Paraíso'), ('FranciscoMorazan', 'Francisco Morazán'), ('GraciasaDios', 'Gracias a Dios'), ('Intibuca', 'Intibucá'), ('IslasdelaBahia', 'Islas de la Bahía'), ('LaPaz', 'La Paz'), ('Lempira', 'Lempira'), ('Ocotepeque', 'Ocotepeque'), ('Olancho', 'Olancho'), ('SantaBarbara', 'Santa Bárbara'), ('Valle', 'Valle'), ('Yoro', 'Yoro')], default='FranciscoMorazan', max_length=500, null=True, verbose_name='Departamento #3'),
        ),
    ]
