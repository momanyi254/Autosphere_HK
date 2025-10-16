from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_garage, name='add_garage'),
    path('list/', views.get_all_garages, name='get_all_garages'),
    path('detail/<int:pk>/', views.get_garage_detail, name='get_garage_detail'),
    path('update/<int:pk>/', views.update_garage, name='update_garage'),
    path('delete/<int:pk>/', views.delete_garage, name='delete_garage'),

    path('add_service/', views.add_service, name='add_service'),
    path('service_list/<int:garage_id>/',
         views.get_services_by_garage, name='get_services_by_garage'),

    path('create_booking/', views.create_booking, name='create_booking'),
    path('get_user_bookings/', views.get_user_bookings, name='get_user_bookings'),
]
