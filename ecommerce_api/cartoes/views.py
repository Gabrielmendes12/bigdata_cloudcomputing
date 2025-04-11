from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from cartoes.models import CartaoCredito
from cartoes.serializers import CartaoCreditoSerializer


class CartaoCreditoViewSet(ModelViewSet):
    queryset = CartaoCredito.objects.all()
    serializer_class = CartaoCreditoSerializer

    # GET /cartoes/<id>/get_saldo/
    @action(detail=True, methods=['get'], url_path='get_saldo')
    def get_saldo(self, request, pk=None):
        try:
            cartao = CartaoCredito.objects.get(pk=pk)
            if cartao.saldo <= 0:
                return Response({"mensagem": "Saldo insuficiente"})
            return Response({"Saldo": cartao.saldo})
        except:
            return Response({"erro": "Cartão não encontrado"}, status=404)

    # POST /cartoes/<id>/autorizacao/
    @action(detail=True, methods=['post'], url_path='autorizacao')
    def autorizacao(self, request, pk=None):
        try:
            print("Recebendo requisição...")
            cartao = CartaoCredito.objects.get(pk=pk)
            print(f"Cartão encontrado: {cartao.id_cartao}")

            valor = request.data.get("valor")
            print(f"Valor recebido: {valor}")

            if valor is None:
                return Response({"erro": "Informe o valor da transação"}, status=400)

            valor = float(valor)
            print(f"Saldo atual: {cartao.saldo}")

            if cartao.saldo is None or cartao.saldo < valor:
                return Response({"mensagem": "Saldo insuficiente"}, status=402)

            cartao.saldo -= valor
            cartao.save()

            print(f"Novo saldo: {cartao.saldo}")

            return Response({"mensagem": "Transação autorizada", "novo_saldo": cartao.saldo}, status=200)

        except CartaoCredito.DoesNotExist:
            return Response({"erro": "Cartão não encontrado"}, status=404)
