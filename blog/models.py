from django.db import models
from django.utils import timezone
import os
from django.core.validators import MaxValueValidator, MinValueValidator
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
import django_filters


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    instructions = models.TextField(blank = True, null = True, default = '')
    title = models.CharField(max_length=200) #title can be the max of 200 characters
    description = models.TextField(max_length=150, blank=False, help_text="Short summary for All recipes page", null=True, )
    image = VersatileImageField(upload_to='post_image', blank=False, null=True)
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
    cookingtime = models.CharField(verbose_name=_('Cooking Time'),default=0, max_length=3, help_text="Please enter time in minutes", blank = False)
    CATEGORY_TYPES = (
        ('Vegan', 'Vegan'),
        ('Dessert', 'Dessert'),
        ('Quick', 'Quick'),
        ('Dinner', 'Dinner'),
        ('Soup', 'Soup'),
        ('Salad', 'Salad'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_TYPES, blank = False, null=True, help_text="Please enter the category of your recipe. It will be displayed on All recipes page.")

    seen = models.BigIntegerField(default=0, editable=False)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def increase(self):
        x = int(self.seen)
        x += 1
        self.seen = x
        self.save(update_fields=["seen"])
        return self.seen


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
        ('piece', 'piece'),
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
    step_number = models.IntegerField(default = 0)
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



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profilePicture = VersatileImageField(verbose_name=_('Profile Picture'),upload_to='post_image', blank=False, null=True)
    birthDate = models.DateField(verbose_name=_('Date Of Birth'),null=True, blank=True, help_text="Please use the following format: year-month-day")
    def age(self):
            import datetime
            dob = self.birthDate
            tod = datetime.date.today()
            age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
            return age
    description = models.TextField(default='', max_length=300, help_text="Tell other users about yourself")
    height = models.IntegerField( blank=True, null=True, default=0,
        validators=[MaxValueValidator(300), MinValueValidator(0)], help_text="Please enter your height in centimeters")
    weight = models.FloatField(blank=True, null=True, default=0,
        validators=[MaxValueValidator(300), MinValueValidator(0)], help_text="Please enter your weight in kilograms" )
    def bmi(self):
        w = self.weight
        h = self.height
        bmi = w/(h/100*h/100)
        return round(bmi,1)
    def heighttInM (self):
        w = self.height/100
        return w

    ALLERGY_CHOICES = (
    ('Milk', 'Milk'),
    ('Tree nut', 'Tree nut'),
    ('Egg', 'Egg'),
    ('Wheat', 'Wheat'),
    ('Gluten', 'Gluten'),
    ('Peanut', 'Peanut'),
    ('Soy', 'Soy'),
    ('Sesame', 'Sesame'),
    ('Other', 'Other'),
)
    allergies = models.CharField(max_length=200, choices=ALLERGY_CHOICES, blank=False, null=True)

    DIETARY_CHOICES = (
    ('Vegan', 'Vegan'),
    ('Lacto Vegetarian', 'Lacto Vegetarian'),
    ('Ovo Vegetarian', 'Ovo Vegetarian'),
    ('Lacto-ovo vegetarian', 'Lacto-ovo vegetarian'),
)
    vegetariantype = models.CharField(verbose_name=_('Vegetarian Type'), max_length=200, choices=DIETARY_CHOICES, blank=False, null=True)

    GENDER_CHOICES = (
    ('Female','Female'),
    ('Male', 'Male'),
    )
    
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=False, null=True, help_text="This information is needed to calculate your daily calorie intake")

    def __str__(self):
        return self.user.username
    
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


            
post_save.connect(create_profile, sender=User)

   

class Friend (models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name = 'owner', null= True)
    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

