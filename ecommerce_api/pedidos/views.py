from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Pedido
from .serializers import PedidoSerializer
from .cosmosdb import cosmos_pedidos

from produtos.cosmosdb import cosmos_produtos
from produtos.models import Produto # aplicação que armazena os produtos no COSMOS DB
from cartoes.models import CartaoCredito  # aplicação que armazena os cartões no MYSQL

@api_view(['POST'])
def criar_pedido(request):
    """
    Recebe JSON com:
      - produto_id
      - numero_cartao
    Busca o cartão (MySQL), o produto (CosmosDB) e cria o pedido.
    """
    serializer = PedidoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    produto_id = serializer.validated_data['produto_id']
    numero_cartao = serializer.validated_data['numero_cartao']

    # 1) Buscar o cartão e extrair id do usuário
    try:
        cartao = CartaoCredito.objects.get(numero=numero_cartao)
        id_usuario = str(cartao.usuario.id)
    except CartaoCredito.DoesNotExist:
        return Response({"erro": "Cartão não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # 2) Buscar o produto e extrair valor
    try:
        # use o método get_item que você definiu no cosmosdb de produtos
        item = cosmos_produtos.get_item(produto_id, partition_key_value=None)
        produto = Produto.from_dict(item)
    except Exception:
        return Response({"erro": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # 3) Criar o Pedido em memória
    pedido = Pedido(
        produto_id=produto.id,
        valor=produto.preco,
        id_pedidousuario=id_usuario,
        numero_cartao=numero_cartao
    )

    # 4) Gravar no Cosmos DB
    try:
        cosmos_pedidos.create_item(pedido.to_dict())
    except Exception as e:
        return Response({"erro": "Falha ao gravar pedido: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 5) Retornar ao cliente
    out_serializer = PedidoSerializer(pedido.to_dict())
    return Response(out_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def listar_pedidos_por_usuario(request, id_pedidousuario):
    """
    GET /pedidos/id_pedidousuario/
    Após a compra no bot, capturamos id_pedidousuario que é o id do usuário dono do cartão, para listar todos os pedidos desse usuário.
    """
    try:
        items = cosmos_pedidos.list_by_usuario(id_pedidousuario)    
        pedidos = [Pedido.from_dict(item) for item in items]
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"erro": "Falha ao listar pedidos: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)