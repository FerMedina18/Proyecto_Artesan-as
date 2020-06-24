from django.shortcuts import render, redirect
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

def index(request):
    # messages.success(request, "Todo bien")
    object_list =[
        {'get_category_display':"Ropa",
         'title':"camisa",
         'get_label_display':"Primary",
         'discount_price':23,
         'price':50
        },
        {'get_category_display':"Madera",
         'title':"Mesa",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':40
        },
        {'get_category_display':"Barro",
         'title':"Jarron",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':60
        },
        {'get_category_display':"Instrumento",
         'title':"Guitarra",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':80
        }
    ]
    return render(request, 'index.html', {'object_list' : object_list})

def condiciones(request):
    return render(request, 'general/condicionesdeuso.html')

def politica(request):
    return render(request, 'general/politicaprivacidad.html')

def productos(request):
    object_list =[
        {'get_category_display':"Ropa",
         'title':"camisa",
         'get_label_display':"Primary",
         'discount_price':23,
         'price':50
        },
        {'get_category_display':"Madera",
         'title':"Mesa",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':40
        },
        {'get_category_display':"Barro",
         'title':"Jarron",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':60
        },
        {'get_category_display':"Instrumento",
         'title':"Guitarra",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':80
        },{'get_category_display':"Ropa",
         'title':"camisa",
         'get_label_display':"Primary",
         'discount_price':23,
         'price':50
        },
        {'get_category_display':"Madera",
         'title':"Mesa",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':40
        },
        {'get_category_display':"Barro",
         'title':"Jarron",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':60
        },
        {'get_category_display':"Instrumento",
         'title':"Guitarra",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':80
        },
        {'get_category_display':"Barro",
         'title':"Jarron",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':60
        },
        {'get_category_display':"Instrumento",
         'title':"Guitarra",
         'get_label_display':"Primary",
         'discount_price':0,
         'price':80
        }
    ]
    return render(request, 'productos.html', {'object_list' : object_list})

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
        form = CrearUsuario(data=request.POST)
        form1 = CrearPerfilVendedor(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = "vendedor"
            user.save()
            
            if form1.is_valid():
                i = Usuario.objects.last()
                profile = form1.save(commit=False)
                profile.estado = True
                profile.user = i
                profile.save()

            if user is not None and profile is not None:
                do_login(request, user)

                return redirect('/')

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    form.fields['email'].help_text = None
    
    return render(request, "cuentas/registro.html", {'form': form, 'form1': form1})

def registro_comprador(request):
    form = CrearUsuario()
    form1 = CrearPerfilComprador()
    if request.method == "POST":
        form = CrearUsuario(data=request.POST)
        form1 = CrearPerfilComprador(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = "comprador"
            user.save()

            if form1.is_valid():
                i = Usuario.objects.last()
                profile = form1.save(commit=False)
                profile.user = i
                profile.estado = True
                profile.save()

            if user is not None and profile is not None:
                do_login(request, user)

                return redirect('/')

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
        form = EditarPerfilComprador(request.POST, instance=profile)
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
        form = EditarPerfilVendedor(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos de tu perfil han sido actualizados')
            return redirect('/editar_perfil_vendedor')

    else:
        form = EditarPerfilVendedor(instance=profile)

    return render(request, "cuentas/editar-perfil-vendedor.html", {'form': form})


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
