# Generated by Django 4.2 on 2023-04-18 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_cart_color_cart_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='color',
            field=models.CharField(default='Белый', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.CharField(default='One', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(default='Белый', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(default='One', max_length=20, null=True),
        ),
    ]
