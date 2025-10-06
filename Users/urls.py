from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('get_users/', views.get_users, name='get_users'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
