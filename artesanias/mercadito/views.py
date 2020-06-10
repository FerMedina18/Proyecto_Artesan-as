from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import HttpResponse

from django.conf import settings
import stripe

def index(request):
   categorias = Categoria.objects.all()
   for cat in categorias:
      if cat.nombre == "Desinfectantes":
         categoria = cat
      else:
          categoria = "Hola"
   return render(request, 'index.html')
# def inicio_sesion(request):
#     return render(request, 'cuentas/inicionormal.html')

@csrf_protect
def inicio_sesion(request):
   # csrfContext = RequestContext(request)
   if request.method == "POST":
       user = Usuario_Vendedor.objects.all()
       for usuario in user:
          if usuario.nombre_usuario == request.POST.get("nusuario") and usuario.contraseña == request.POST.get("pusuario"):
             return render(request, 'index.html')
          else: 
            render(request, 'cuentas/inicionormal.html')

   else:            
      return render(request, 'cuentas/inicionormal.html')

#para stripe
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Camiseta',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '1500',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

# def registrar(request):
#    if request.method == "POST":
#       form = PostLogin(request.POST)
#       if form.is_valid():
#          post = form.save(commit=False)
#          post.nombre_usuario = request.nusuario
#          post.contraseña = request.pusuario
#          post.save()
#          return redirect('index')
      
#       else:
#          form = PostLogin()
#       return render(request, '/templates/cuentas/inicionormal.html', {'form': form})


# @api_view(["GET"])
# @csrf_exempt
# @permission_classes([IsAuthenticated]) 
# def welcome(request):
#    content = {"message": "Welcome to the Mercadito de Artesanías"}
#    return JsonResponse(content)

# @api_view(["GET"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def get_usuario_vendedor(request):
#    user = request.user.id
#    usuario_vendedor = Usuario_Vendedor(added_by=user)
#    serializer = UVendedorSerializer
#    return JsonResponse({'usuario_vendedor': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_usuario_vendedor(request):
#    user = request.user.id
#    usuario_comprador = Usuario_Comprador(added_by=user)
#    serializer = UCompradorSerializer
#    return JsonResponse({'usuario_comprador': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_perfil_vendedor(request):
#    user = request.user.id
#    perfil_vendedor = Perfil_Vendedor(added_by=user)
#    serializer = PVendedorSerializer
#    return JsonResponse({'perfil_vendedor': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_perfil_comprador(request):
#    user = request.user.id
#    perfil_comprador = Perfil_Comprador(added_by=user)
#    serializer = PCompradorSerializer
#    return JsonResponse({'perfil_comprador': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_producto(request):
#    user = request.user.id
#    producto = Producto(added_by=user)
#    serializer = ProductoSerializer
#    return JsonResponse({'producto': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_categoria(request):
#    user = request.user.id
#    categoria = Categoria(added_by=user)
#    serializer = CategoriaSerializer
#    return JsonResponse({'categoria': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_producto_categoria(request):
#    user = request.user.id
#    producto_categoria = Producto_Categoria(added_by=user)
#    serializer = Producto_CatSerializer
#    return JsonResponse({'producto_categoria': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_imagen(request):
#    user = request.user.id
#    imagen = Imagen(added_by=user)
#    serializer = ImagenSerializer
#    return JsonResponse({'imagen': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_puntuacion(request):
#    user = request.user.id
#    puntuacion = Puntuacion(added_by=user)
#    serializer = PuntuacionSerializer
#    return JsonResponse({'puntuacion': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_orden(request):
#    user = request.user.id
#    orden = Orden(added_by=user)
#    serializer = OrdenSerializer
#    return JsonResponse({'orden': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_detalle_orden(request):
#    user = request.user.id
#    detalle_orden = Detalle_Orden(added_by=user)
#    serializer = DOrdenSerializer
#    return JsonResponse({'detalle_orden': serializer.data}, safe=False, status=status.HTTP_200_OK)
