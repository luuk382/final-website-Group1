from django.db import models
from django.utils import timezone
import os
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200) #title can be the max of 200 characters 
    text = models.TextField()
    description = models.TextField(max_length=100, blank=False, null=True)
    image = models.ImageField(upload_to='post_image', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    text = models.TextField()
    DIFFICULTY_LEVELS = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Difficult', 'Difficult'),
    )
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, blank = False)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    cookingtime = models.CharField(default=0, max_length=3, help_text="Please enter time in minutes", blank = False)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


