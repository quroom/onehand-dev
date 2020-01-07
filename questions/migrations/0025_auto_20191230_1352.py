# Generated by Django 2.1.3 on 2019-12-30 13:52

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0024_auto_20191230_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pros_category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('REB', '중개'), ('TAX', '세무'), ('RES', '등기'), ('LAW', '법률'), ('LON', '대출'), ('INR', '인테리어'), ('CLN', '청소'), ('MOV', '이사'), ('PRC', '입주사전점검'), ('HAP', '가전구매'), ('FRP', '가구구매')], default='NA', max_length=43),
        ),
    ]
