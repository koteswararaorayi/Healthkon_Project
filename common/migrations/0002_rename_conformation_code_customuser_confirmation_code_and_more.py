# Generated by Django 4.1.1 on 2022-09-27 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='conformation_code',
            new_name='confirmation_code',
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='newusers',
        ),
    ]