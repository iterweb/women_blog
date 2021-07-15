# Generated by Django 3.2.5 on 2021-07-14 06:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('women', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
    ]