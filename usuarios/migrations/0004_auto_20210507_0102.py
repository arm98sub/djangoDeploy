# Generated by Django 3.1.6 on 2021-05-07 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20210506_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estado',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
