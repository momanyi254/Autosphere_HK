from django.urls import path
from . import views

urlpatterns = [
    # CREATE
    path('addRentalCar/', views.addRentalCar, name='addRentalCar'),

    # READ
    path('get_all_cars/', views.get_all_cars, name='get_all_cars'),
    path('get_car/<int:car_id>/', views.get_car, name='get_car'),

    # UPDATE
    path('update_car/<int:car_id>/', views.update_car, name='update_car'),

    # DELETE
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
]
