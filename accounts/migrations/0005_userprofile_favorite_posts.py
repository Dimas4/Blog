# Generated by Django 2.0.3 on 2018-07-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_auto_20180706_1403'),
        ('accounts', '0004_auto_20180706_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favorite_posts',
            field=models.ManyToManyField(blank=True, to='post.Posts'),
        ),
    ]
