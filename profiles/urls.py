from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
]
