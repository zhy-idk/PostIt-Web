from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.urls import reverse
from api.models import PostModel

def homepage(request):
    post = PostModel.objects.all().order_by('-created_at')
    return render(request, "web/home.html", {"posts": post})

@login_required
def new_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        user = request.user
        banner = request.FILES.get("banner")
        post = PostModel(title=title, description=description, user=user, banner=banner)
        post.save()
        return redirect(reverse('homepage'))
    return render(request, "web/new_post.html")

@login_required
def edit_post(request, post_id):
    post = PostModel.objects.get(id=post_id)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.description = request.POST.get("description")
        if 'banner' in request.FILES:
            post.banner = request.FILES['banner']
        post.save()
        return redirect(reverse('homepage'))
    return render(request, "web/edit_post.html", {"post": post})

@login_required
def delete_post(request, post_id):
    post = PostModel.objects.get(id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect(reverse('homepage'))
    return render(request, "web/edit_post.html", {"post": post})

def post_detail(request, post_id):
    post = PostModel.objects.get(id=post_id)
    return render(request, "web/post_detail.html", {"post": post})

@login_required
def user_post(request, user_id):
    post = PostModel.objects.filter(user_id=user_id).order_by('-created_at')
    return render(request, "web/user_post.html", {"posts": post})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "web/login.html")
    else:
        form = UserCreationForm()
    return render(request, "web/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('homepage'))
    else:
        form = AuthenticationForm()
    return render(request, "web/login.html", {"form": form})

@login_required
def logout_view(request):
    if request.method == "POST": 
        logout(request)
        return redirect(reverse('homepage'))