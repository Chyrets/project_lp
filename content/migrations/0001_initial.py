# Generated by Django 4.0 on 2021-12-23 13:32

import content.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_alter_profile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.profile', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('caption', models.TextField(max_length=4000, verbose_name='Содержание')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=content.models.user_directory_path, verbose_name='Изображение')),
                ('publication_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('changed', models.BooleanField(default=False, verbose_name='Изменен')),
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('modification_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Автор')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='content.Tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]