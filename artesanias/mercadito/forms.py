from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm

class UsuarioLogin(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password')

class CrearUsuario(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'avatar', 'password1', 'password2')

class ModificarUsuario(PasswordChangeForm):
    class Meta:
        model = Usuario
        fields = ('old_password', 'new_password1', 'new_password2')

class CrearPerfilVendedor(forms.ModelForm):
    class Meta:
        model = Perfil_Vendedor
        fields = ('portada', 'nombres', 'apellidos', 'ciudad', 
                  'telefono', 'direccion', 'descripcion')

class CrearPerfilComprador(forms.ModelForm):
    class Meta:
        model = Perfil_Comprador
        fields = ('nombres', 'apellidos', 'ciudad', 
                  'telefono', 'direccion', 'descripcion')

class EditarPerfilComprador(forms.ModelForm):
    class Meta:
        model = Perfil_Comprador
        fields = ('nombres', 'apellidos', 'ciudad', 
                  'telefono', 'direccion', 'descripcion')

class EditarPerfilVendedor(forms.ModelForm):
    class Meta:
        model = Perfil_Vendedor
        fields = ('portada', 'nombres', 'apellidos', 'ciudad', 
                  'telefono', 'direccion', 'descripcion')

class AgregarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'precio', 'existencia', 
                  'descripcion', 'estado')

class ImagenProducto(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ('ruta',)

class EditarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'precio', 'existencia', 'descripcion')