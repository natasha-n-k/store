# Generated by Django 4.2 on 2023-12-28 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('clothing', 'Clothing'), ('accessories', 'Accessories')], default='Clothing', max_length=20, null=True),
        ),
    ]