# Generated by Django 2.0.6 on 2018-06-08 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='social.jpg', null=True, upload_to='media'),
        ),
    ]