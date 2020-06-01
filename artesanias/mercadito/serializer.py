from .models import *
from rest_framework import serializers

class UVendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario_Vendedor
        fields = ('__all__')

class PVendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil_Vendedor
        fields = ('__all__')

class UCompradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario_Comprador
        fields = ('__all__')

class PCompradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil_Comprador
        fields = ('__all__')


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('__all__')

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('__all__')

class Producto_CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto_Categoria
        fields = ('__all__')

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ('__all__')

class PuntuacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puntuacion
        fields = ('__all__')

class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ('__all__')

class DOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Orden
        fields = ('__all__')



