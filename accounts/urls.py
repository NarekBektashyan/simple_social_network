from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('profile/<str:pk>/', views.profile, name='profile'),
]
