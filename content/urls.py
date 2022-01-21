from django.urls import path

from . import views

app_name = 'content'
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('posts/<slug:profile_slug>/', views.ProfilePostsView.as_view(), name='profile_posts_list'),
    path('posts-by-tag/<slug:tag>/', views.PostsByTagView.as_view(), name='posts_by_tag'),
    path('post-detail/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('add-post/', views.AddPostView.as_view(), name='add_post'),
    path('edit-post/<int:post_id>/', views.EditPostView.as_view(), name='edit_post'),
    path('delete-post/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('post-reaction/<int:post_id>/<int:reaction>/', views.PostReactionView.as_view(), name='post_reaction'),
    path('post/<int:post_id>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('edit-comment/<int:comment_id>/', views.EditCommentView.as_view(), name='edit_comment'),
    path('delete-comment/<int:comment_id>/', views.DeleteCommentView.as_view(), name='delete_comment')
]
