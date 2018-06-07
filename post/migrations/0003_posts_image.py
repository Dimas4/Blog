# Generated by Django 2.0.6 on 2018-06-05 14:08

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20180603_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=post.models.generate_image_path, width_field='width_field'),
        ),
    ]