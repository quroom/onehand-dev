# Generated by Django 2.1.3 on 2019-12-13 18:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0009_auto_20191210_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='voters',
            field=models.ManyToManyField(related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
    ]
