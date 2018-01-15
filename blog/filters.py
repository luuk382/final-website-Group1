from django.contrib.auth.models import User
from .models import Post
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['difficulty', 'category' ]


class PostDifficultyFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['difficulty' ]