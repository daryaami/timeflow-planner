# Generated by Django 5.1.3 on 2025-02-22 14:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCalendar',
            fields=[
                ('calendar_id', models.CharField(help_text='Идентификатор календаря из Google.', max_length=255, primary_key=True, serialize=False)),
                ('summary', models.CharField(help_text='Название календаря, как отображается у пользователя.', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Описание календаря, если доступно.', null=True)),
                ('owner', models.BooleanField(blank=True, default=True, help_text='Является ли пользователь владельцем календаря.')),
                ('background_color', models.CharField(blank=True, help_text='Цвет календаря в формате HEX (например, #ff0000).', max_length=7, null=True)),
                ('selected', models.BooleanField(default=True, help_text='Флаг, указывающий выбран ли календарь для отображения.')),
                ('time_zone', models.CharField(blank=True, help_text='Часовой пояс календаря.', max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendars', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Календарь пользователя',
                'verbose_name_plural': 'Календари пользователей',
                'unique_together': {('user', 'calendar_id')},
            },
        ),
    ]
