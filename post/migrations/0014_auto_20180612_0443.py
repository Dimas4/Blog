# Generated by Django 2.0.6 on 2018-06-12 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_remove_posts_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='rate',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
