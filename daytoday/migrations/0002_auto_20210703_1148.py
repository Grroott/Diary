# Generated by Django 3.2.5 on 2021-07-03 06:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('daytoday', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='content',
            field=models.TextField(max_length=30000),
        ),
        migrations.AlterField(
            model_name='daily',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 7, 3, 6, 18, 51, 874970, tzinfo=utc)),
        ),
    ]
