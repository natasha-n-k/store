# Generated by Django 4.1 on 2023-03-28 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
