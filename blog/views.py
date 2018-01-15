import json

from .models import Post, Comment, UserProfile, Friend, Ingredient, Step
from .forms import (
    PostForm, 
    CommentForm, 
    EditProfileForm,
    ProfileForm
    )
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.db.models.functions import Cast
from django.contrib.auth.models import User

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer  
from .filters import UserFilter, PostFilter, PostDifficultyFilter


# Will only show published posts
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_categories(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'blog/post_categories.html', {'filter': post_filter})


def home(request):
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html')

def gallery(request):
    return render(request, 'blog/gallery.html')

def vegan(request):
    post_list = Post.objects.filter(category="Vegan").order_by('published_date')
    post_filter = PostDifficultyFilter(request.GET, queryset=post_list)
    posts = Post.objects.filter(category="Vegan").order_by('published_date')
    return render(request, 'blog/vegan.html', {'posts': posts, 'filter': post_filter})

def dessert(request):
    post_list = Post.objects.filter(category="Dessert").order_by('published_date')
    post_filter = PostDifficultyFilter(request.GET, queryset=post_list)
    posts = Post.objects.filter(category="Dessert").order_by('published_date')
    return render(request, 'blog/dessert.html', {'posts': posts, 'filter': post_filter})

def quick(request):
    post_list = Post.objects.filter(category="Quick").order_by('published_date')
    post_filter = PostDifficultyFilter(request.GET, queryset=post_list)
    posts = Post.objects.filter(category="Quick").order_by('published_date')
  
    return render(request, 'blog/quick.html', {'posts': posts,'filter': post_filter})

def dinner(request):
    post_list = Post.objects.filter(category="Dinner").order_by('published_date')
    post_filter = PostDifficultyFilter(request.GET, queryset=post_list)
    posts = Post.objects.filter(category="Dinner").order_by('published_date')
    return render(request, 'blog/dinner.html', {'posts': posts, 'filter': post_filter})

def soup(request):
    post_list = Post.objects.filter(category="Soup").order_by('published_date')
    post_filter = PostDifficultyFilter(request.GET, queryset=post_list)
    posts = Post.objects.filter(category="Soup").order_by('published_date')
    return render(request, 'blog/soup.html', {'posts': posts, 'filter': post_filter})

def salad(request):
    post_list = Post.objects.filter(category="Salad").order_by('published_date')
    post_filter = PostDifficultyFilter(request.GET, queryset=post_list)
    posts = Post.objects.filter(category="Salad").order_by('published_date')
    return render(request, 'blog/salad.html', {'posts': posts, 'filter': post_filter})
  

# If there is a post, it's opened in post_detail.html or an error
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Means that login is required to edit these fields


@login_required
def post_new(request):
    measurement_units = [u[0] for u in Ingredient.MEASUREMENT_UNITS]

    if request.method == "POST":

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            ingredients = json.loads(request.POST['ingredients'])
            steps = json.loads(request.POST['steps'])

            for ingredient in ingredients.values():
                if ingredient != "":
                    i = Ingredient()
                    i.title = ingredient["description"]
                    i.quantity = ingredient["amount"]
                    i.measurement = ingredient["unit"]
                    i.post = post
                    i.save()

            for number, step in enumerate(steps):
                s = Step()
                s.step_number = number + 1
                s.description = step
                s.post = post
                s.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(
                request,
                'blog/post_edit.html',
                {'form': form, 'test_var': measurement_units}
            )



@login_required
def profile(request,pk):
    profile = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/profile.html', {'user': profile, 'posts': posts})

@login_required
def profile_settings(request, pk):
    profile = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditProfileForm(request.POST,  request.FILES, instance=profile)
        #form = ProfileForm(request.POST,  request.FILES, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('profile', pk=profile.pk)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'blog/profile_settings.html', {'form': form})

@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST,  request.FILES, instance=profile)
        #form = ProfileForm(request.POST,  request.FILES, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('profile', pk=profile.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile_edit.html', {'form': form})

def change_friend(request,operation,pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend )
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend )
    return redirect('about')

@login_required
def friends_list(request, pk):
    users = User.objects.exclude(id = request.user.id)
    friend = Friend.objects.get(current_user = request.user, pk=pk)
    friends = friend.users.all()
    return render(request, 'blog/friends.html', {'users': users, 'friends': friends})



@login_required
def password(request,pk):
    password = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=password)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile', pk=profile.pk)
        else: 
            return redirect('password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'blog/password_change.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ingredient = Ingredient.objects.filter(post = post) 
    measurement_units = [u[0] for u in Ingredient.MEASUREMENT_UNITS]
    if request.method == "POST":
        form = PostForm(request.POST,  request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            ingredients = json.loads(request.POST['ingredients'])
            steps = json.loads(request.POST['steps'])

            for ingredient in ingredients.values():
                if ingredient != "":
                    i = Ingredient()
                    i.title = ingredient["description"]
                    i.quantity = ingredient["amount"]
                    i.measurement = ingredient["unit"]
                    i.post = post
                    i.save()

            for number, step in enumerate(steps):
                s = Step()
                s.step_number = number + 1
                s.description = step
                s.post = post
                s.save()


            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'test_var': measurement_units})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author_user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



class PostList(APIView):
    def get(self, request): # For GET requests
        posts = Post.objects.all().order_by('published_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self): # For POST requests
        pass



class CommentList(APIView):
    def get(self, request): # For GET requests
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def post(self): # For POST requests
        pass


 
