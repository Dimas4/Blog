# Generated by Django 2.0.6 on 2018-06-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
