#Agora, ajustamos a view do Django para retornar os produtos diretamente do Cosmos DB.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .cosmosdb import cosmos_produtos
from .models import Produto
from .serializers import ProdutoSerializer

@api_view(['GET'])
def listar_produtos(request):
    items = cosmos_produtos.list_items()
    produtos = [Produto.from_dict(item) for item in items]
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def buscar_produto_por_nome(request):
    nome = request.GET.get("productName", "").lower()
    items = cosmos_produtos.list_items()
    produtos = [Produto.from_dict(item) for item in items if nome in item.get("nome", "").lower()]
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)

# Nova view adicionada pro bot -> Isso faz um filtro básico por nome (insensível a maiúsculas/minúsculas) entre os produtos retornados do Cosmos DB.

@api_view(['POST'])
def criar_produto(request):
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        produto = Produto(**serializer.validated_data)
        cosmos_produtos.create_item(produto.to_dict())
        return Response(produto.to_dict(), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def atualizar_produto(request, id):
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        produto = Produto(**serializer.validated_data, id=id)
        cosmos_produtos.update_item(id, produto.to_dict())
        return Response(produto.to_dict())
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deletar_produto(request, id, categoria):
    #categoria = request.data.get("categoria")  # precisa da partition key
    if not categoria:
        return Response({"error": "Campo 'categoria' é obrigatório para deletar o item."}, status=400)
    cosmos_produtos.delete_item(id, categoria)
    return Response(status=status.HTTP_204_NO_CONTENT)
