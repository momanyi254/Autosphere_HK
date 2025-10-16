from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Garage, Service, Booking
from .serializers import GarageSerializer, ServiceSerializer, BookingSerializer


# GARAGE VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_garage(request):
    serializer = GarageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_garages(request):
    garages = Garage.objects.all()
    serializer = GarageSerializer(garages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_garage_detail(request, pk):
    try:
        garage = Garage.objects.get(pk=pk)
    except Garage.DoesNotExist:
        return Response({'error': 'Garage not found'}, status=404)
    serializer = GarageSerializer(garage)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_garage(request, pk):
    try:
        garage = Garage.objects.get(pk=pk)
    except Garage.DoesNotExist:
        return Response({'error': 'Garage not found'}, status=404)
    serializer = GarageSerializer(garage, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_garage(request, pk):
    try:
        garage = Garage.objects.get(pk=pk)
    except Garage.DoesNotExist:
        return Response({'error': 'Garage not found'}, status=404)
    garage.delete()
    return Response({'message': 'Garage deleted successfully'}, status=200)


# 🧰 SERVICE VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_service(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_services_by_garage(request, garage_id):
    services = Service.objects.filter(garage_id=garage_id)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


# 📅 BOOKING VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
