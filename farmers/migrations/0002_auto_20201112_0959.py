# Generated by Django 3.1.2 on 2020-11-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pintolatlong',
            name='pin',
            field=models.IntegerField(),
        ),
    ]
