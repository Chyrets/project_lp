from django.urls import path

from . import views


app_name = 'followers'
urlpatterns = [
    path('follow/<slug:profile_slug>/<int:option>/', views.FollowView.as_view(), name='follow')
]
