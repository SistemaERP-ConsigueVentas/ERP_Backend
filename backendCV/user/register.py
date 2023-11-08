from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            apellidos = request.POST.get('apellidos')
            email = request.POST.get('email')
            password = request.POST.get('password')
            username = request.POST.get('username')
            
            # Cifra la contraseña
            hashed_password = make_password(password)

            # Crea un nuevo usuario
            user = User(nombre=nombre, apellidos=apellidos, email=email, password=hashed_password, username=username)
            user.save()

            return JsonResponse({'message': 'Usuario registrado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Envía una solicitud POST con datos JSON para registrarte'}, status=400)
