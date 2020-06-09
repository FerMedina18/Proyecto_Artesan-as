from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializer import *
from .models import *
from rest_framework import status


def index(request):
   categorias = Categoria.objects.all()
   return render(request, 'index.html', {'categorias': categorias})


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
