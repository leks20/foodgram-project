# Generated by Django 3.1.1 on 2020-09-08 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200907_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.IntegerField(verbose_name='Время приготовления'),
        ),
    ]
