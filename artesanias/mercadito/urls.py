from django.urls import path
from .views import index
from  rest_framework import routers
from .viewsets import *
from .views import *

app_name = 'mercadito'

urlpatterns = [
    path('', index, name='home'),
    # path('get_usuario_vendedor', get_usuario_vendedor),
    # path('get_categoria', get_categoria)
]

router = routers.SimpleRouter()
router.register('Usuario_Vendedor', UVendedor_ViewSet),
router.register('Perfil_Vendedor', PVendedor_ViewSet),
router.register('Usuario_Comprador', UComprador_ViewSet),
router.register('Perfil_Comprador', PComprador_ViewSet),
router.register('Producto', Producto_ViewSet),
router.register('Categoria', Categoria_ViewSet),
router.register('Producto_Categoria', ProductoCat_ViewSet),
router.register('Image', Imagen_ViewSet),
router.register('Puntuacion', Puntuacion_ViewSet),
router.register('Orden', Orden_ViewSet),
router.register('Detalle_Orden', DOrden_ViewSet),

urlpatterns = router.urls