from django import forms
from .models import *

class PostLogin(forms.ModelForm):
    class Meta:
        model = Usuario_Vendedor
        fields = ('nombre_usuario', 'contraseña')