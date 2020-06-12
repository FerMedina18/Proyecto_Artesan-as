from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.base_user import BaseUserManager


# Create your models here.

# class UserManager(BaseUserManager):
#     use_in_migrations = True
    
#     def _create_user(self, nombre_usuario, correo, contraseña, **extra_fields):
#         if not nombre_usuario:
#             raise ValueError('Debe ingresar el usuario')
#         correo = self.normalize_email(correo)
#         nombre_usuario = self.model(nombre_usuario=nombre_usuario, **extra_fields)
#         nombre_usuario.set_password(contraseña)
#         nombre_usuario.save(using=self._db)
#         return nombre_usuario

#     def create_user(self, nombre_usuario, correo, contraseña=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(nombre_usuario, correo, contraseña, **extra_fields)
    
#     def create_superuser(self, nombre_usuario, correo, contraseña, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True')

#         return self._create_user(nombre_usuario, correo, contraseña, **extra_fields)

class Usuario_Vendedor(AbstractUser):
    avatar = models.ImageField(blank=True)

    # objects = UserManager()

    # USERNAME_FIELD = 'usuario'
    # REQUIRED_FIELDS = []

    # class Meta:
    #     verbose_name = _('user')
    #     verbose_plural_name = _('users')

    # def get_full_name(self):
    #     full_name = '%s' % (self.nombre_usuario)
    #     return full_name.strip()

    # def get_short_name(self):
    #     short_name = '%s' % (self.nombre_usuario)
    #     return short_name.strip()

    # def email_user(self, subject, message, from_mail=None, **kwargs):
    #     send_mail(subject, message, from_mail, [self.correo], **kwargs)

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

    # def __str__(self):
    #     return self.usuario_comprador

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

