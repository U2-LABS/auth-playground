# Generated by Django 3.1.3 on 2020-11-26 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20201125_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='refresh_token',
        ),
    ]
