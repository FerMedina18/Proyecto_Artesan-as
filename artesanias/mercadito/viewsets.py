from rest_framework import viewsets
from .models import *
from .serializer import *

class Usuario_ViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PVendedor_ViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Vendedor.objects.all()
    serializer_class = PVendedorSerializer

class PComprador_ViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Comprador.objects.all()
    serializer_class = PCompradorSerializer

class Producto_ViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class Categoria_ViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoCat_ViewSet(viewsets.ModelViewSet):
    queryset = Producto_Categoria.objects.all()
    serializer_class = Producto_CatSerializer

class Imagen_ViewSet(viewsets.ModelViewSet):
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer

class Puntuacion_ViewSet(viewsets.ModelViewSet):
    queryset = Puntuacion.objects.all()
    serializer_class = PuntuacionSerializer

class Order_ViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItem_ViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer