# Generated by Django 2.0.6 on 2018-06-11 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20180608_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='category',
        ),
    ]