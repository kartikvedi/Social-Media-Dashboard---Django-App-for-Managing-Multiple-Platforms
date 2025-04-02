from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, SocialMediaPost, ScheduledPost
import requests
from datetime import datetime
from django.utils.timezone import now

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = CustomUser.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("dashboard")
    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")

@login_required
def dashboard(request):
    posts = SocialMediaPost.objects.filter(user=request.user)
    scheduled_posts = ScheduledPost.objects.filter(user=request.user, posted=False)
    return render(request, "dashboard.html", {"posts": posts, "scheduled_posts": scheduled_posts})

@login_required
def fetch_twitter_posts(request):
    user = request.user
    if user.twitter_token:
        response = requests.get("https://api.twitter.com/2/tweets", headers={"Authorization": f"Bearer {user.twitter_token}"})
        if response.status_code == 200:
            tweets = response.json()
            for tweet in tweets.get("data", []):
                SocialMediaPost.objects.create(user=user, platform="Twitter", content=tweet["text"])
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "No Twitter token found"})

@login_required
def fetch_facebook_posts(request):
    user = request.user
    if user.facebook_token:
        response = requests.get(f"https://graph.facebook.com/me/posts?access_token={user.facebook_token}")
        if response.status_code == 200:
            posts = response.json()
            for post in posts.get("data", []):
                SocialMediaPost.objects.create(user=user, platform="Facebook", content=post.get("message", "No content"))
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "No Facebook token found"})
