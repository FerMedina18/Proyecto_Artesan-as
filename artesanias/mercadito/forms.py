from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class UsuarioLogin(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password')

class CrearUsuario(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'avatar')

class ModificarUsuario(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'password')

class CrearPerfilVendedor(forms.ModelForm):
    class Meta:
        model = Perfil_Vendedor
        fields = ('portada', 'nombres', 'apellidos', 'ciudad', 
        'telefono', 'direccion', 'descripcion')

class CrearPerfilComprador(forms.ModelForm):
    class Meta:
        model = Perfil_Vendedor
        fields = ('nombres', 'apellidos', 'ciudad', 
        'telefono', 'direccion', 'descripcion')
