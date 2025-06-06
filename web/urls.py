from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.homepage, name="homepage"),
    path("new_post/", views.new_post, name="new_post"),
    path("post_detail/<int:post_id>/", views.post_detail, name="post_detail"),
    path("user_post/<int:user_id>/", views.user_post, name="user_post"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("sign_in/", views.register, name="register"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
]