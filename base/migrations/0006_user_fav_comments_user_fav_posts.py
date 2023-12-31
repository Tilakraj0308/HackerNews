# Generated by Django 4.2.1 on 2023-06-06 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_comment_up_users_post_up_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fav_comments',
            field=models.ManyToManyField(related_name='fav_by', to='base.comment'),
        ),
        migrations.AddField(
            model_name='user',
            name='fav_posts',
            field=models.ManyToManyField(related_name='fav_by', to='base.post'),
        ),
    ]
