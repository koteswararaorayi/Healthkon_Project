# Generated by Django 4.1.1 on 2022-09-27 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_myuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
