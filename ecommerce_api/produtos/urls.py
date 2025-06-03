from django.urls import path
from .views import listar_produtos, criar_produto, atualizar_produto, deletar_produto, buscar_produto_por_nome

urlpatterns = [
    path("produtos/", listar_produtos, name="listar_produtos"),
    path("produto/", criar_produto, name="criar_produto"),
    path("produto/<str:id>/", atualizar_produto, name="atualizar_produto"),
    path("produto/<str:id>/<str:categoria>/", deletar_produto, name="deletar_produto"),
    path("produtos/search", buscar_produto_por_nome, name="buscar_produto_por_nome"),  # <-- NOVA ROTA PRO BOT
]

#Adicionei as rotas GET /produtos/ e POST /produto/ separadamente.