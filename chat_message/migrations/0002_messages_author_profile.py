# Generated by Django 2.0.6 on 2018-06-13 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180608_1450'),
        ('chat_message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='author_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile'),
            preserve_default=False,
        ),
    ]
