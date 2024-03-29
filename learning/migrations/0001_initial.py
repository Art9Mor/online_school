# Generated by Django 5.0.1 on 2024-01-24 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Название не указано', max_length=120, verbose_name='Название курса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='learning/', verbose_name='Первью')),
                ('description', models.TextField(blank=True, default='Описание появится в скором времени', null=True, verbose_name='Описание курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Название урока')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание урока')),
                ('image', models.ImageField(blank=True, null=True, upload_to='learning/', verbose_name='Первью')),
                ('video', models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ['course'],
            },
        ),
    ]
