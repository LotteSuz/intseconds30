# Generated by Django 2.2.5 on 2019-09-11 19:28

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190911_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaySession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(auto_now=True)),
                ('secret', models.CharField(default=api.models.random_secret, max_length=16)),
                ('used_cards', models.ManyToManyField(to='api.Card')),
            ],
        ),
    ]