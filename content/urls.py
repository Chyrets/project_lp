from django.urls import path

from . import views

app_name = 'content'
urlpatterns = [
    path('posts/<slug:profile_slug>/', views.ProfilePostsView.as_view(), name='profile_posts_list')
]
