from django.urls import path
from . import views

urlpatterns = [
    path('add_car/', views.add_car, name='add_car'),
    path('get_cars/', views.get_cars, name='get_cars'),
     path('get_car/<int:car_id>/', views.get_car, name='get_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
]
