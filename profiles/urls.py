from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profiles/', views.UserProfilesView.as_view(), name='profiles'),
    path('profiles/add_profile/', views.AddUserProfileView.as_view(), name='add_profile'),
    path('profiles/<slug:profile_slug>/', views.EditUserProfileView.as_view(), name='edit_profile'),
    path('profiles/delete/<slug:profile_slug>/', views.DeleteUserProfile.as_view(), name='delete_profile')
]
