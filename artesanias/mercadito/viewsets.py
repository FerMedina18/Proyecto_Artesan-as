from rest_framework import viewsets
from .models import *
from .serializer import *

class UVendedor_ViewSet(viewsets.ModelViewSet):
    queryset = Usuario_Vendedor.objects.all()
    serializer_class = UVendedorSerializer

class PVendedor_ViewSet(viewsets.ModelViewSet):
    queryset = Perfil_Vendedor.objects.all()
    serializer_class = PVendedorSerializer

class UComprador_ViewSet(viewsets.ModelViewSet):
    queryset = Usuario_Comprador.objects.all()
    serializer_class = UCompradorSerializer

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

class Orden_ViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class DOrden_ViewSet(viewsets.ModelViewSet):
    queryset = Detalle_Orden.objects.all()
    serializer_class = DOrdenSerializer



