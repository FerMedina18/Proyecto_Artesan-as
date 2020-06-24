from django.urls import path, include
from .views import index
from  rest_framework import routers
from .viewsets import *
from .views import *
from . import views
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registro_vendedor/', registro_vendedor, name='registro_vendedor'),
    path('registro_comprador/', registro_comprador, name='registro_comprador'),
    path('editar_usuario', editar_usuario, name='editar_usuario'),
    path('editar_perfil_comprador', editar_perfil_comprador, name='editar_perfil_comprador'),
    path('editar_perfil_vendedor', editar_perfil_vendedor, name='editar_perfil_vendedor'),
    path('condiciones/', views.condiciones, name='condiciones'),
    path('politica/', views.politica, name='politica'),
    path('productos/', views.productos, name='productos'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('images/favicon.ico'),
            permanent=False),
        name='favicon'
    ),
    # path('get_Usuario', get_Usuario),
    # path('get_categoria', get_categoria)
]

router = routers.SimpleRouter()
router.register('Usuario', Usuario_ViewSet),
router.register('Perfil_Vendedor', PVendedor_ViewSet),
router.register('Perfil_Comprador', PComprador_ViewSet),
router.register('Producto', Producto_ViewSet),
router.register('Categoria', Categoria_ViewSet),
router.register('Producto_Categoria', ProductoCat_ViewSet),
router.register('Image', Imagen_ViewSet),
router.register('Puntuacion', Puntuacion_ViewSet),
router.register('Orden', Orden_ViewSet),
router.register('Detalle_Orden', DOrden_ViewSet),
# router.register('Profile', Profile_ViewSet),

urlpatterns += router.urls