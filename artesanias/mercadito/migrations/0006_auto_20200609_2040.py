# Generated by Django 3.0.6 on 2020-06-10 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercadito', '0005_auto_20200602_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='descripcion',
            field=models.TextField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='perfil_comprador',
            name='descripcion',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='perfil_comprador',
            name='direccion',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='perfil_comprador',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='usuarioComprador'),
        ),
        migrations.AlterField(
            model_name='perfil_vendedor',
            name='descripcion',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='perfil_vendedor',
            name='direccion',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(default='', max_length=300),
        ),
    ]
