from django import forms

from .models import Post, Comment, Ingredient

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'description', 'text', 'image', 'cookingtime', 'difficulty','category',  )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('quantity', 'measurement', 'title',)