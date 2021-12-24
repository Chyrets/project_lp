from django.urls import path

from . import views

app_name = 'content'
urlpatterns = [
    path('posts/<slug:profile_slug>/', views.ProfilePostsView.as_view(), name='profile_posts_list'),
    path('post-detail/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('add-post/', views.AddPostView.as_view(), name='add-post')
]
