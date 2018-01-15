
# Register your models here.
from django.contrib import admin
from .models import Post, Comment, Ingredient, Step

admin.site.register(Step)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Ingredient)
