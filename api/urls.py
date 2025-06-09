from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name='login'),
    path("register/", views.register_api, name='register_api'),
    path("logout/", views.logout_api, name='logout'),
    path("posts/", views.get_posts, name="post_list"),
    path("post/<int:post_id>/", views.post_detail_api, name='post_detail_api'),
    path("user_posts/<int:user_id>/", views.user_post_api, name='user_post_api'),
    path("new_post/", views.new_post_api, name="new_post_api"),
    path("edit_post/<int:post_id>/", views.edit_post_api, name='edit_post_api'),
    path("delete/<int:post_id>/", views.delete_post_api, name='delete_post_api'),
]