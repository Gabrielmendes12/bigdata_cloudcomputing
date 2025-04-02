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
from enderecos.views import EnderecoViewSet, TipoEnderecoViewSet
from produtos.views import ProdutoViewSet
from rest_framework import routers

# Criando um router para gerar automaticamente as rotas
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'cartoes', CartaoCreditoViewSet)
router.register(r'enderecos', EnderecoViewSet)
router.register(r'tipos-endereco', TipoEnderecoViewSet)
#router.register(r'pedidos', PedidoViewSet)
router.register(r'produtos', ProdutoViewSet)
#router.register(r'itens-pedido', ItemPedidoViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),

]
