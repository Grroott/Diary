# Generated by Django 3.2.5 on 2021-08-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daytoday', '0006_alter_daily_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='date',
            field=models.DateField(),
        ),
    ]
