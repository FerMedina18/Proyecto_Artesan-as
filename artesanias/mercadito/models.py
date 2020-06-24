from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuario(AbstractUser):
    avatar = models.ImageField(blank=True)
    rol = models.CharField(max_length=20)

class Perfil_Vendedor(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="profile_vendedor")
    portada = models.ImageField(blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    direccion = models.TextField(max_length=300)
    descripcion = models.TextField(default='', max_length=500)
    estado = models.BooleanField(default=True)

class Perfil_Comprador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="profile_comprador")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    direccion = models.TextField(max_length=300)
    descripcion = models.TextField(default='', max_length=500)
    estado = models.BooleanField(default=True)

# @receiver(post_save, sender=Usuario)
# def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        if instance.rol == "vendedor":
#             Perfil_Vendedor.objects.create(user=instance)

#        elif instance.rol == "comprador":
#            Perfil_Comprador.objects.create(user=instance)

# @receiver(post_save, sender=Usuario)
# def save_user_profile(sender, instance, **kwargs):  
#     if instance.rol == "vendedor":
#         instance.profile_vendedor.save()
#     elif instance.rol == "comprador":
#         instance.profile_comprador.save()

class Producto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    existencia = models.PositiveIntegerField(default=0)
    fecha_publicacion = models.DateField(auto_now=True)
    descripcion = models.TextField(default='', max_length=300)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default='', max_length=200)

    def __str__(self):
        return self.nombre

class Producto_Categoria(models.Model):
    producto = models.ManyToManyField(Producto)
    categoria = models.ManyToManyField(Categoria)

class Imagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ruta = models.ImageField(blank=True)

    def __str__(self):
        return self.producto

class Puntuacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario_comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.producto

class Orden(models.Model):
    usuario_comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(auto_now=True)
    fecha_envio = models.DateField(auto_now=False)

class Detalle_Orden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    descuento = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return self.producto

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     descripcion = models.TextField(max_length=500, blank=True)
#     fecha_nacimiento = models.DateField(null=True, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

