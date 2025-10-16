from rest_framework import serializers
from .models import Garage, Service, Booking


class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = '__all__'
        read_only_fields = ['owner'] 


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
