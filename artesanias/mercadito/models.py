from django.db import models

# Create your models here.
class Usuario_Vendedor(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre_usuario

class Perfil_Vendedor(models.Model):
    usuario_vendedor = models.OneToOneField(Usuario_Vendedor, on_delete=models.CASCADE)
    imagen = models.ImageField(blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(unique=True)
    direccion = models.TextField(max_length=300)
    descripcion = models.TextField(default='', max_length=500)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario_vendedor

class Usuario_Comprador(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre_usuario

class Perfil_Comprador(models.Model):
    usuario_comprador = models.OneToOneField(Usuario_Comprador, on_delete=models.CASCADE)
    imagen = models.ImageField(blank=True)
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
    
    
    

