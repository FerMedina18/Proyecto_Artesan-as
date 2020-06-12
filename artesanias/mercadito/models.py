from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuario_Vendedor(AbstractUser):
    avatar = models.ImageField(blank=True)

class Perfil_Vendedor(models.Model):
    user = models.OneToOneField(Usuario_Vendedor, on_delete=models.CASCADE, related_name="profile")
    portada = models.ImageField(blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(unique=True)
    direccion = models.TextField(max_length=300)
    descripcion = models.TextField(default='', max_length=500)
    estado = models.BooleanField(default=True)

@receiver(post_save, sender=Usuario_Vendedor)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil_Vendedor.objects.create(user=instance)

@receiver(post_save, sender=Usuario_Vendedor)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Usuario_Comprador(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre_usuario

class Perfil_Comprador(models.Model):
    usuario_comprador = models.OneToOneField(Usuario_Comprador, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="usuarioComprador", blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(unique=True)
    direccion = models.TextField(max_length=300)
    descripcion = models.TextField(default='', max_length=500)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario_comprador

class Producto(models.Model):
    usuario_vendedor = models.ForeignKey(Usuario_Vendedor, on_delete=models.CASCADE)
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
    usuario_comprador = models.ForeignKey(Usuario_Comprador, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.producto

class Orden(models.Model):
    usuario_comprador = models.ForeignKey(Usuario_Comprador, on_delete=models.CASCADE)
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

