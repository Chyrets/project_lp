# Generated by Django 4.0 on 2022-01-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалён'),
        ),
    ]
