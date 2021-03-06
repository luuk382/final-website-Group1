from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Post, Comment, UserProfile

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'description', 'image', 'cookingtime', 'difficulty', 'category')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

"""
class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('quantity', 'measurement', 'title',)
"""

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'username', 'password')



class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('description', 'profilePicture', 'birthDate', 'gender', 'weight', 'height', 'allergies', 'vegetariantype')

