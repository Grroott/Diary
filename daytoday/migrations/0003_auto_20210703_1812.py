# Generated by Django 3.2.5 on 2021-07-03 12:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('daytoday', '0002_auto_20210703_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 7, 3, 12, 42, 21, 874963, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='daily',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]