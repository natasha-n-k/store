# Generated by Django 4.2 on 2023-04-19 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_cart_color_alter_cart_size_alter_product_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='color',
            field=models.CharField(default='Белый', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='One', max_length=20, null=True),
        ),
    ]
