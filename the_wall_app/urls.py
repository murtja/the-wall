from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('wall', views.show_wall),
    path('post', views.create_a_post),
    path('comment', views.post_a_comment),
    path('delete_message/<int:id>', views.delete_message),
    path('delete_comment/<int:id>', views.delete_comment),
    path('logout', views.logout_user),
]