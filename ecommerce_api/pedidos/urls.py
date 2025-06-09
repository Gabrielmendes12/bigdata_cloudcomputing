from django.urls import path
from .views import criar_pedido, listar_pedidos_por_usuario

# Rotas das operações de pedidos:  # POST /pedido/ e # GET /pedidos/usuario/<id_pedidousuario>/
urlpatterns = [
    path('pedido/', criar_pedido, name='criar_pedido'),
    path('pedidos/usuario/<str:id_pedidousuario>/', listar_pedidos_por_usuario, name='listar_pedidos_por_usuario'),  
]