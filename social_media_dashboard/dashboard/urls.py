from django.urls import path
from .views import home, register, user_login, dashboard, fetch_twitter_posts, fetch_facebook_posts

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("fetch-twitter/", fetch_twitter_posts, name="fetch_twitter"),
    path("fetch-facebook/", fetch_facebook_posts, name="fetch_facebook"),
]
