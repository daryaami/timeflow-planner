# Generated by Django 5.1.3 on 2025-04-05 20:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usercalendar',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendars', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='usercalendar',
            constraint=models.UniqueConstraint(condition=models.Q(('owner', True)), fields=('calendar_id',), name='unique_calendar_id_when_owner_true'),
        ),
    ]
