# Generated by Django 4.2.1 on 2023-06-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_user_fav_comments_user_fav_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
