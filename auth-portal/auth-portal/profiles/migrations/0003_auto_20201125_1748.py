# Generated by Django 3.1.3 on 2020-11-25 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_user_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='access_token'),
        ),
        migrations.AddField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='access_token'),
        ),
    ]