# Generated by Django 3.2.5 on 2021-08-02 13:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('daytoday', '0003_auto_20210703_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
