from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Usuario_Comprador)
admin.site.register(Usuario_Vendedor)
admin.site.register(Perfil_Comprador)
admin.site.register(Perfil_Vendedor)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Producto_Categoria)
admin.site.register(Puntuacion)
admin.site.register(Orden)
admin.site.register(Detalle_Orden)
admin.site.register(Imagen)