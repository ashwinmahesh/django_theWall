from django.db import models
from apps.login_registration.models import *

class PostManager(models.Manager):
    def validate(self, postData):
        errors={}
        if(len(postData['message'])==0):
            errors['post_fail']='You cannot post nothing.'
        return errors

class Post(models.Model):
    content=models.TextField()
    sender_id=models.ForeignKey(User, related_name='posts')
    created_at=models.DateTimeField(auto_now_add=True)

    objects=PostManager()

class CommentManager(models.Manager):
    def validate(self, postData):
        errors={}
        if(len(postData['comment'])==0):
            errors['comment_fail']='Comments cannot be empty'
        return errors

class Comment(models.Model):
    content=models.TextField()
    posted_to=models.ForeignKey(Post, related_name='comments')
    sender_id=models.ForeignKey(User, related_name='comments')
    created_at=models.DateTimeField(auto_now_add=True)
    objects=CommentManager()
# Create your models here.
