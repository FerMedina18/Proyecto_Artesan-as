from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class CustomUserLogin(AuthenticationForm):
    class Meta:
        model = Usuario_Vendedor
        fields = ('username', 'password')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario_Vendedor
        fields = ('username', 'email', 'password1', 'avatar')
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario_Vendedor
        fields = ('username', 'password')

class CustomProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Perfil_Vendedor
        fields = ('portada', 'nombres', 'apellidos', 'ciudad', 
        'telefono', 'direccion', 'descripcion')
