# Generated by Django 4.2.8 on 2023-12-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BHM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bhm', models.IntegerField(default=0)),
                ('car', models.IntegerField(default=0)),
                ('truck', models.IntegerField(default=0)),
            ],
        ),
    ]