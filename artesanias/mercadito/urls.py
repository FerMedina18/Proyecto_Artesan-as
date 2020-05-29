from django.urls import path
from .views import index

app_name = 'mercadito'

urlpatterns = [
    path('', index, name='home')
]