from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth import update_session_auth_hash
from .forms import *
import stripe
from django.contrib import messages

from .models import *
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def index(request):
    #cargar las categorias
    categorias = Categoria.objects.all()

    # messages.success(request, "Todo bien")
    productos = Producto.objects.all()
    p = Producto_Categoria.objects.all()
    imagen = Imagen.objects.all()

    context = {
        'p' : p,
        'categorias':categorias,
        'imagen':imagen
    }
    
    return render(request, 'index.html', context)


def condiciones(request):
    #cargar las categorias
    categorias = Categoria.objects.all()

    context = {
        'categorias':categorias
    }
    return render(request, 'general/condicionesdeuso.html', context)

def politica(request):
    #cargar las categorias
    categorias = Categoria.objects.all()

    context = {
        'categorias':categorias
    }
    return render(request, 'general/politicaprivacidad.html')


# Usando clases
class pagprod(DetailView):
    model = Producto
    template_name = "paginaproducto.html"

class PagEditarProducto(DetailView):
    model = Producto
    template_name = "editarproducto.html"

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Se han actulizado las cantidades.")
            return redirect("mercadito:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Se ha agregado un nuevo producto a tu carrito.")
            return redirect("mercadito:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Se ha agregado un nuevo producto a tu carrito.")
        return redirect("mercadito:order-summary")

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No hay ordenes activas.")
            return redirect("/")

@login_required
def add_to_cart(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        producto=producto,
        user=request.user,
        ordered=False
    )
    # query selector
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # varifica si un producto esta en lista
        if order.productos.filter(producto__slug=producto.slug).exists():
            if order_item.cantidad < producto.existencia:
                order_item.cantidad += 1
                order_item.save()
                messages.info(request, "Se han actulizado las cantidades.")
                return redirect("mercadito:order-summary")
            else:
                messages.info(request, "Ya no hay mas productos disponibles.")
                return redirect("mercadito:order-summary")
        else:
            order.productos.add(order_item)
            messages.info(request, "Se ha agregado un nuevo producto a tu carrito.")
            return redirect("mercadito:order-summary")
    else:
        fecha_pedido = timezone.now()
        order = Order.objects.create(
            user=request.user, fecha_pedido=fecha_pedido)
        order.productos.add(order_item)
        messages.info(request, "Se ha agregado un nuevo producto a tu carrito.")
        return redirect("mercadito:order-summary")

@login_required
def remove_from_cart(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # verificar que estan ordenada las ordenes de los productos
        if order.productos.filter(producto__slug=producto.slug).exists():
            order_item = OrderItem.objects.filter(
                producto=producto,
                user=request.user,
                ordered=False
            )[0]
            order.productos.remove(order_item)
            order_item.delete()
            messages.info(request, "El producto fue removido de su carrito.")
            return redirect("mercadito:order-summary")
        else:
            messages.info(request, "")
            return redirect("mercadito:producto", slug=slug)
    else:
        messages.info(request, "No tiene ningun pedido activo")
        return redirect("mercadito:producto", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.productos.filter(producto__slug=producto.slug).exists():
            order_item = OrderItem.objects.filter(
                producto=producto,
                user=request.user,
                ordered=False
            )[0]
            if order_item.cantidad > 1:
                order_item.cantidad -= 1
                order_item.save()
            else:
                order.productos.remove(order_item)
            messages.info(request, "Las unidades del producto han sido actualizadas.")
            return redirect("mercadito:order-summary")
        else:
            messages.info(request, "Este producto no estaba en tu carrito")
            return redirect("mercadito:producto", slug=slug)
    else:
        messages.info(request, "No hay predidos activos")
        return redirect("mercadito:producto", slug=slug)

def agregar_producto(request):
    #cargar las categorias
    categorias = Categoria.objects.all()

    context = {
        'categorias':categorias
    }

    if request.POST:
        producto = Producto()

        usuario = Usuario()
        usuario.id = request.user.id

        producto.usuario = usuario
        
        #El nombre compadre
        producto.nombre = request.POST.get('pnombre')
        producto.precio = float(request.POST.get('pprecio'))
        producto.descuento = float(request.POST.get('pexistencias'))
        producto.existencia = int(request.POST.get('pexistencias'))
        producto.descripcion = request.POST.get('pdescripcion')
        producto.slug = producto.nombre

        try:
            producto.save()

            imagen = Imagen()

            imagen.producto = producto
            imagen.ruta = request.FILES.get('iproducto')

            imagen.save()
            
            prod_categ = Producto_Categoria()
            # Hay que guardarlo primero
            prod_categ.slug = producto.nombre
            prod_categ.save()
            prod_categ.producto.add(producto)

            for c in Categoria.objects.all():
                if c.id == int(request.POST.get('pcategorias')):
                    prod_categ.categoria.add(c)

            try:
                messages.success(request, "Guardado correctamente")
            except:
                messages.success(request, "No se pudo guardar")
        except:
            messages.success(request, "No se pudo guardar")

    return render(request, 'agregarproducto.html', context)

def editar_producto(request):
    categorias = Categoria.objects.all()

    context = {
        'categorias':categorias
    }

    if request.POST:
        producto = Producto()

        usuario = Usuario()
        usuario.id = request.user.id

        producto.usuario = usuario
        
        #El nombre compadre
        producto.nombre = request.POST.get('pnombre')
        producto.precio = request.POST.get('pprecio')
        producto.existencia = request.POST.get('pexistencias')
        producto.descripcion = request.POST.get('pdescripcion')
        producto.slug = producto.nombre

        try:
            producto.save()

            imagen = Imagen()

            imagen.producto = producto
            imagen.ruta = request.FILES.get('iproducto')

            imagen.save()
            
            prod_categ = Producto_Categoria()
            # Hay que guardarlo primero
            prod_categ.slug = producto.nombre
            prod_categ.save()
            prod_categ.producto.add(producto)

            for c in Categoria.objects.all():
                if c.id == int(request.POST.get('pcategorias')):
                    prod_categ.categoria.add(c)

            try:
                messages.success(request, "Guardado correctamente")
            except:
                messages.success(request, "No se pudo guardar")
        except:
            messages.success(request, "No se pudo guardar")

    return render(request, 'editarproducto.html', context)


def mi_perfilc(request):
    #cargar las categorias
    categorias = Categoria.objects.all()

    context = {
        'categorias':categorias
    }
    return render(request, 'miperfilc.html', context)

def mi_perfilv(request):
    #cargar las categorias
    categorias = Categoria.objects.all()

    context = {
        'categorias':categorias
    }
    return render(request, 'miperfilv.html', context)

def productos(request):
    #cargar las categorias
    categorias = Categoria.objects.all()

    productos = Producto.objects.all()
    p = Producto_Categoria.objects.all()
    imagen = Imagen.objects.all()

    context = {
        'p' : p,
        'categorias':categorias,
        'imagen':imagen
    }

    return render(request, 'productos.html', {'object_list' : object_list, 'categorias':categorias})

@csrf_protect
def login(request):
    csrfContext = RequestContext(request)
    p = "nada"
    form = UsuarioLogin()
    if request.method == "POST":
        form = UsuarioLogin(data=request.POST)
        p = request.POST['tipo']
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(p)


            user = authenticate(username = username, password = password)

            if user is not None:
                do_login(request, user)

                return redirect('/')
    return render(request, "cuentas/login.html", {'form': form, 'p': p})

def logout(request):
    do_logout(request)

    return redirect('/')

def registro_vendedor(request):
    form = CrearUsuario()
    form1 = CrearPerfilVendedor()
    if request.method == "POST":
        form = CrearUsuario(data=request.POST and request.FILES)
        form1 = CrearPerfilVendedor(data=request.POST and request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = "vendedor"
            try:
                user.save()
            except:
                messages.error(request, "El usuario que ingreso ya existe o el correo ya esta asociado a otro usuario...")

            if form1.is_valid():
                i = Usuario.objects.last()
                profile = form1.save(commit=False)
                profile.estado = True
                profile.user = i
                try:
                    profile.save()
                except:
                    messages.error(request, "Error al registrar perfil...")

            if user is not None and profile is not None:
                do_login(request, user)

                return redirect('/')

        else:
            messages.error(request, "Error al registrarse, verifique los campos y vuelva intentarlo...")

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    form.fields['email'].help_text = None
    
    return render(request, "cuentas/registro.html", {'form': form, 'form1': form1})

def registro_comprador(request):
    form = CrearUsuario()
    form1 = CrearPerfilComprador()
    if request.method == "POST":
        form = CrearUsuario(request.POST, request.FILES)
        form1 = CrearPerfilComprador(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = "comprador"
            try:
                user.save()
            except:
                messages.error(request, "El usuario ya existe o el correo ya esta asociado a otro usuario...")

            if form1.is_valid():
                i = Usuario.objects.last()
                profile = form1.save(commit=False)
                profile.user = i
                profile.estado = True
                try:
                    profile.save()
                except:
                    messages.error(request, "Error al registrar perfil...")

            if user is not None and profile is not None:
                do_login(request, user)

                return redirect('/')

        else:
            messages.error(request, "Error al registrarse, verifique los campos y vuelva intentarlo...")

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    form.fields['email'].help_text = None
    
    return render(request, "cuentas/registrocomprador.html", {'form': form, 'form1': form1})

# @login_required
def editar_usuario(request):
    if request.method == 'POST':
        form = ModificarUsuario(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada')
            return redirect('/editar_usuario')

        else:
            messages.error(request, 'Error al actualizar la contraseña, verifique los campos y vuelva a intentarlo...')

    else:
        form = ModificarUsuario(request.user)

    return render(request, "cuentas/editar-usuario.html", {'form': form})

def editar_perfil_comprador(request):
    form = EditarPerfilComprador()
    profile = Perfil_Comprador.objects.get(user=request.user)
    if request.method == "POST":
        form = EditarPerfilComprador(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos de tu perfil han sido actualizados')
            return redirect('/editar_perfil_comprador')
    else:
        form = EditarPerfilComprador(instance=profile)
    
    return render(request, "cuentas/editar-perfil-comprador.html", {'form': form})

def editar_perfil_vendedor(request):
    form = EditarPerfilVendedor()
    profile = Perfil_Vendedor.objects.get(user=request.user)
    if request.method == "POST":
        form = EditarPerfilVendedor(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos de tu perfil han sido actualizados')
            return redirect('/editar_perfil_vendedor')

    else:
        form = EditarPerfilVendedor(instance=profile)

    return render(request, "cuentas/editar-perfil-vendedor.html", {'form': form})

    
def ver_productos(request):
    product = list()

    for producto in Producto.objects.all():
        if producto.usuario == request.user:
            product.append({
                'id': producto.id,
                'ruta': producto.get_imagen,
                'nombre': producto.nombre,
                'categoria': producto.get_categoria,
                'precio': producto.precio,
                'existencia': producto.existencia,
                'descripcion': producto.descripcion,
                'get_url': producto.get_absolute_url,
                 })

    return render(request, 'mis-productos.html', {'product': product})

def listar_categoria(request):
    categoria = Categoria.objects.all()

    return render(request, "editarproducto.html", {'categoria': categoria})


#para stripe
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'Nombre': 'Camiseta',
                        'Cantidad': 1,
                        'Moneda': 'usd',
                        'Costo': '1500',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

# @api_view(["GET"])
# @csrf_exempt
# @permission_classes([IsAuthenticated]) 
# def welcome(request):
#    content = {"message": "Welcome to the Mercadito de Artesanías"}
#    return JsonResponse(content)

# @api_view(["GET"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def get_Usuario(request):
#    user = request.user.id
#    Usuario = Usuario(added_by=user)
#    serializer = UVendedorSerializer
#    return JsonResponse({'Usuario': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_Usuario(request):
#    user = request.user.id
#    usuario = usuario(added_by=user)
#    serializer = UCompradorSerializer
#    return JsonResponse({'usuario': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_perfil_vendedor(request):
#    user = request.user.id
#    perfil_vendedor = Perfil_Vendedor(added_by=user)
#    serializer = PVendedorSerializer
#    return JsonResponse({'perfil_vendedor': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_perfil_comprador(request):
#    user = request.user.id
#    perfil_comprador = Perfil_Comprador(added_by=user)
#    serializer = PCompradorSerializer
#    return JsonResponse({'perfil_comprador': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_producto(request):
#    user = request.user.id
#    producto = Producto(added_by=user)
#    serializer = ProductoSerializer
#    return JsonResponse({'producto': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_categoria(request):
#    user = request.user.id
#    categoria = Categoria(added_by=user)
#    serializer = CategoriaSerializer
#    return JsonResponse({'categoria': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_producto_categoria(request):
#    user = request.user.id
#    producto_categoria = Producto_Categoria(added_by=user)
#    serializer = Producto_CatSerializer
#    return JsonResponse({'producto_categoria': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_imagen(request):
#    user = request.user.id
#    imagen = Imagen(added_by=user)
#    serializer = ImagenSerializer
#    return JsonResponse({'imagen': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_puntuacion(request):
#    user = request.user.id
#    puntuacion = Puntuacion(added_by=user)
#    serializer = PuntuacionSerializer
#    return JsonResponse({'puntuacion': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_orden(request):
#    user = request.user.id
#    orden = Orden(added_by=user)
#    serializer = OrdenSerializer
#    return JsonResponse({'orden': serializer.data}, safe=False, status=status.HTTP_200_OK)

# def get_detalle_orden(request):
#    user = request.user.id
#    detalle_orden = Detalle_Orden(added_by=user)
#    serializer = DOrdenSerializer
#    return JsonResponse({'detalle_orden': serializer.data}, safe=False, status=status.HTTP_200_OK)
