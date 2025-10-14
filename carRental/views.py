from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Car


# CREATE


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addRentalCar(request):
    try:
        data = request.data
        image = request.FILES.get('image')

        required_fields = ['name', 'brand', 'year', 'cc', 'price']
        missing_fields = [f for f in required_fields if not data.get(f)]
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        car = Car.objects.create(
            owner=request.user,
            name=data.get('name'),
            brand=data.get('brand'),
            year=int(data.get('year')),
            cc=int(data.get('cc')),
            price=data.get('price'),
            description=data.get('description', ''),
            image=image
        )

        return Response(
            {"message": "Car created successfully", "car": car.to_dict()},
            status=status.HTTP_201_CREATED
        )

    except ValueError as e:
        return Response({"error": f"Invalid data type: {str(e)}"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)



# READ - ALL


@api_view(['GET'])
def get_all_cars(request):
    cars = list(Car.objects.values(
        'id', 'name', 'brand', 'cc', 'price', 'description'))
    if not cars:
        return JsonResponse({"message": "No car found"}, status=404)
    return JsonResponse({"cars": cars}, status=200)


# READ - SINGLE


@api_view(['GET'])
def get_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        return JsonResponse({"car": car.to_dict()}, status=200)
    except Car.DoesNotExist:
        return JsonResponse({"error": "Car not found"}, status=404)



# UPDATE


@api_view(['PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id, owner=request.user)
        data = request.data

        for field in ['name', 'brand', 'year', 'cc', 'price', 'description']:
            if field in data:
                setattr(car, field, data[field])
        if 'image' in request.FILES:
            car.image = request.FILES['image']

        car.save()
        return JsonResponse({"message": "Car updated successfully", "car": car.to_dict()}, status=200)

    except Car.DoesNotExist:
        return JsonResponse({"error": "Car not found or not owned by user"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# DELETE


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id, owner=request.user)
        car.delete()
        return JsonResponse({"message": "Car deleted successfully"}, status=200)
    except Car.DoesNotExist:
        return JsonResponse({"error": "Car not found or not owned by user"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
