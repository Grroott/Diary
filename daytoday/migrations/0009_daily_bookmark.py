# Generated by Django 3.2.5 on 2021-08-14 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daytoday', '0008_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily',
            name='bookmark',
            field=models.BooleanField(default=False),
        ),
    ]