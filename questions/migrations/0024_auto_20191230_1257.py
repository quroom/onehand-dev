# Generated by Django 2.1.3 on 2019-12-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0023_auto_20191230_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='moving_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
