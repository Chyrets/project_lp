# Generated by Django 4.0 on 2022-01-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='used',
            field=models.BooleanField(default=False, verbose_name='Используется'),
        ),
    ]