# Generated by Django 4.2.1 on 2023-07-21 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_post_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='upvote',
        ),
        migrations.RemoveField(
            model_name='post',
            name='upvote',
        ),
    ]
