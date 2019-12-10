# Generated by Django 2.1.3 on 2019-12-10 16:06

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20191210_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='item_category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, '원룸'), (2, '투룸'), (3, '쓰리룸'), (4, '포룸'), (5, '쉐어하우스'), (11, '오피스텔'), (21, '아파트'), (22, '빌라'), (23, '단독주택'), (24, '상가주택'), (31, '상가'), (41, '토지')], default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='trade_category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, '매매'), (2, '전세'), (3, '월세'), (4, '교환')], default=1, max_length=7),
            preserve_default=False,
        ),
    ]
