"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios.views import UsuarioViewSet 
from cartoes.views import CartaoCreditoViewSet
from enderecos.views import EnderecoViewSet
from rest_framework import routers

# Criando um router para gerar automaticamente as rotas
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'cartoes', CartaoCreditoViewSet, basename='cartao')
router.register(r'enderecos', EnderecoViewSet)

# Usuários (singular)
usuario_create = UsuarioViewSet.as_view({'post': 'create'})
usuario_detail = UsuarioViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

# Cartões (singular)
cartao_create = CartaoCreditoViewSet.as_view({'post': 'create'})
cartao_detail = CartaoCreditoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

# Endereços (singular)
endereco_create = EnderecoViewSet.as_view({'post': 'create'})
endereco_detail = EnderecoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('produtos.urls')),
    path("", include('pedidos.urls')),
    path('', include(router.urls)),

    # Usuários
    path('usuario/', usuario_create, name='usuario-create'),
    path('usuario/<str:pk>/', usuario_detail, name='usuario-detail'),

    # Cartões
    path('cartao/', cartao_create, name='cartao-create'),
    path('cartao/<str:pk>/', cartao_detail, name='cartao-detail'),

    # Endereços
    path('endereco/', endereco_create, name='endereco-create'),
    path('endereco/<str:pk>/', endereco_detail, name='endereco-detail'),
]

