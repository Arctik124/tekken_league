# Generated by Django 3.1.3 on 2020-11-25 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0002_auto_20201125_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='player1_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='battle',
            name='player2_score',
            field=models.IntegerField(default=0),
        ),
    ]
