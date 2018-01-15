
# Register your models here.
from django.contrib import admin
from .models import Post, Comment, UserProfile, Friend, Ingredient, Step


admin.site.register(Step)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Friend)
admin.site.register(Ingredient)
