from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('delProfile/', views.delProfile, name='delProfile'),
]