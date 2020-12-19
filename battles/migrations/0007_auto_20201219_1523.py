# Generated by Django 3.1.3 on 2020-12-19 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0006_battle_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='delta',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='battle',
            name='winner',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
