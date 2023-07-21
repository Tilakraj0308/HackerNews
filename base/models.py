from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import auth

# Create your models here.

class User(AbstractUser):
    name = models.TextField(max_length=200, null=True)
    username = models.TextField(max_length=200, null=False, unique=True)
    email = models.EmailField(null=True)
    about = models.TextField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    fav_posts = models.ManyToManyField('Post', related_name='fav_by')
    fav_comments = models.ManyToManyField('Comment', related_name='fav_by')

    def __str__(self):
        return self.username
    
    def getType(self):
        return "User"



class Post(models.Model):
    title = models.TextField(max_length=200, null=False)
    url = models.URLField(null=False, unique=True)
    body = models.TextField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # upvote = models.IntegerField(default=0)
    up_users = models.ManyToManyField(User, related_name='upvoted_posts')
    
    def __str__(self):
        return self.title[:50]
    
    def getType(self):
        return "Post"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    body = models.TextField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    # upvote = models.IntegerField(default=0)
    up_users = models.ManyToManyField(User, related_name='upvoted_comments')

    def __str__(self):
        return self.body[:50]
    
    def getType(self):
        return "Comment"
    
    class Meta:
        ordering = ['-created']

    

