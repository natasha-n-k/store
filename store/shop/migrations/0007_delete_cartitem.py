# Generated by Django 4.1 on 2023-03-30 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_delete_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
