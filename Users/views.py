import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# REGISTER ENDPOINT
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            password1 = data.get('password1')
            password2 = data.get('password2')
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not username or not email or not password1 or not password2:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password1)
        #json reponse

        response_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'message': f'welcome, {user.username}!'
            }
        
        return JsonResponse(response_data, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# LOGIN ENDPOINT
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': f'Welcome back, {user.username}'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# GET ALL USERS (ADMIN ONLY)
@login_required
def get_users(request):
    if request.method == 'GET':
        if not request.user.is_superuser:
            return JsonResponse({"error": "Access denied. Admins only."}, status=403)

        users = User.objects.all().values(
            "id", "username", "email", "is_staff", "is_superuser",
            "date_joined", "last_login"
        )
        return JsonResponse({"users": list(users)}, safe=False, status=200)

    return JsonResponse({'error': 'Invalid request method. Use GET.'}, status=405)


# DELETE USER
@login_required
@csrf_exempt
def delete_user(request, user_id):
    if request.method == "DELETE":
        try:
            user_to_delete = User.objects.get(id=user_id)
        except Exception:
            return JsonResponse({"error": "User not found"}, status=404)

        if request.user.id == user_to_delete.id:
            user_to_delete.delete()
            return JsonResponse({"message": "Your account has been deleted successfully"}, status=200)

        if request.user.is_superuser:
            user_to_delete.delete()
            return JsonResponse({"message": f"Account for {user_to_delete.username} deleted by admin"}, status=200)

        return JsonResponse({"error": "Permission denied"}, status=403)

    return JsonResponse({'error': 'Invalid request method. Use DELETE.'}, status=405)
