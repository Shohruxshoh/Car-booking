# Generated by Django 4.2.8 on 2023-12-24 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_rename_date_booking_dat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='dat',
            new_name='date',
        ),
    ]
