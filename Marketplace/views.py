import json
from django.http import JsonResponse
from .models import Car
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# CREATE CAR
@csrf_exempt
@login_required
def add_car(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            car = Car.objects.create(
                name=data.get('name'),
                brand=data.get('brand'),
                condition=data.get('condition'),
                year=data.get('year'),
                price=data.get('price')
            )

            return JsonResponse({
                "message": "Car created successfully",
                "car": {
                    "id": car.id,
                    "name": car.name,
                    "brand": car.brand,
                    "condition": car.condition,
                    "year": car.year,
                    "price": str(car.price),
                    "created_at": car.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": car.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)


# READ ALL CARS
def get_cars(request):
    if request.method == "GET":
        cars = Car.objects.all().values(
            'id', 'name', 'year', 'brand', 'condition', 'price'
        )
        return JsonResponse({"cars": list(cars)}, status=200, safe=False)

    return JsonResponse({'error': 'Invalid request method. Use GET.'}, status=405)


# READ SINGLE CAR
def get_car(request, car_id):
    if request.method == "GET":
        try:
            car = Car.objects.values(
                'id', 'name', 'year', 'brand', 'condition', 'price'
            ).get(id=car_id)
            return JsonResponse({"car": car}, status=200)
        except Car.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)

    return JsonResponse({'error': 'Invalid request method. Use GET.'}, status=405)


# UPDATE CAR
@csrf_exempt
@login_required
def update_car(request, car_id):
    if request.method == "PUT":
        try:
            car = Car.objects.get(id=car_id)
            data = json.loads(request.body.decode('utf-8'))

            # update fields if provided
            car.name = data.get('name', car.name)
            car.brand = data.get('brand', car.brand)
            car.condition = data.get('condition', car.condition)
            car.year = data.get('year', car.year)
            car.price = data.get('price', car.price)
            car.save()

            return JsonResponse({
                "message": f"Car {car_id} updated successfully",
                "car": {
                    "id": car.id,
                    "name": car.name,
                    "brand": car.brand,
                    "condition": car.condition,
                    "year": car.year,
                    "price": str(car.price),
                    "created_at": car.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": car.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            }, status=200)

        except Car.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method. Use PUT.'}, status=405)


# DELETE CAR
@csrf_exempt
@login_required
def delete_car(request, car_id):
    if request.method == "DELETE":
        try:
            car_to_delete = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)

        if not request.user.is_superuser:
            return JsonResponse({"error": "Permission denied. Admins only."}, status=403)

        car_to_delete.delete()
        return JsonResponse({"message": f"Car {car_id} deleted successfully"}, status=200)

    return JsonResponse({'error': 'Invalid request method. Use DELETE.'}, status=405)
