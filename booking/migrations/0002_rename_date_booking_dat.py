# Generated by Django 4.2.8 on 2023-12-24 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='date',
            new_name='dat',
        ),
    ]
