# Generated by Django 3.1.2 on 2020-11-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PinToLatLong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.IntegerField(max_length=6)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
            ],
        ),
    ]