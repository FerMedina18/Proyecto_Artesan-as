from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *


# Register your models here.
from .models import *

# class CustomUserAdmin(UserAdmin):
#     add_form = CrearUsuario
#     form = ModificarUsuario
#     model = Usuario
#     list_display = ['username', 'password']


admin.site.register(Usuario)
admin.site.register(Perfil_Comprador)
admin.site.register(Perfil_Vendedor)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Producto_Categoria)
admin.site.register(Puntuacion)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Imagen)
# admin.site.unregister(Usuario)
# admin.site.register(Usuario, CustomUserAdmin)