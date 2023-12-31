# Generated by Django 4.2.1 on 2023-06-05 14:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_post_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='up_users',
            field=models.ManyToManyField(related_name='upvoted_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='up_users',
            field=models.ManyToManyField(related_name='upvoted_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
