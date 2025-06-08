from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("posts/", views.get_posts, name="post_list"),
    path("user_posts/<int:user_id>/", views.user_post_api, name="user_post_api"),
    path("new_post/", views.new_post_api, name="new_post_api"),
]