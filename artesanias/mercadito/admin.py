from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *


# Register your models here.
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario_Vendedor
    list_display = ['username', 'password']

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
admin.site.unregister(Usuario_Vendedor)
admin.site.register(Usuario_Vendedor, CustomUserAdmin)