from django.db import models
from django.utils import timezone
import os
from django.core.validators import MaxValueValidator, MinValueValidator
from versatileimagefield.fields import VersatileImageField

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200) #title can be the max of 200 characters
    description = models.TextField(max_length=150, blank=False, help_text="Short summary for All recipes page", null=True, )
    image = VersatileImageField(upload_to='post_image', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    DIFFICULTY_LEVELS = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Difficult', 'Difficult'),
    )
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, blank = False)
    qty = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
     )
    cookingtime = models.CharField(default=0, max_length=3, help_text="Please enter time in minutes", blank = False)
    CATEGORY_TYPES = (
        ('Vegan', 'Vegan'),
        ('Dessert', 'Dessert'),
         ('Quick', 'Quick'),
        ('Dinner', 'Dinner'),
        ('Soup', 'Soup'),
        ('Salad', 'Salad'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_TYPES, blank = False, null=True, help_text="Please enter the category of your recipe. It will be displayed on All recipes page.")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    quantity = models.CharField(max_length=10)
    MEASUREMENT_UNITS = (
        ('tbsp', 'tbsp'),
        ('tsp', 'tsp'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('tsp', 'tsp'),
        ('ml', 'ml'),
        ('l', 'l'),
    )
    measurement = models.CharField(max_length=200, choices=MEASUREMENT_UNITS, blank=True, null=True)
    post = models.ForeignKey('blog.Post', related_name='ingredients')

    def publish(self):
        self.save()


    def __str__(self):
        return self.title


class Step(models.Model):
    description = models.CharField(max_length=300)
    step_number = models.IntegerField()
    post = models.ForeignKey('blog.Post', related_name='steps')

    def publish(self):
        self.save()

    def __str__(self):
        return self.description

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    author_user = models.ForeignKey('auth.User',  blank=False, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
