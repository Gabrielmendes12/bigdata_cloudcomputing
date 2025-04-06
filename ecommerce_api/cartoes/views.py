from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from cartoes.models import CartaoCredito
from cartoes.serializers import CartaoCreditoSerializer
from rest_framework.decorators import action

# Create your views here.
class CartaoCreditoViewSet(ModelViewSet):
    queryset = CartaoCredito.objects.all()
    serializer_class = CartaoCreditoSerializer

    @action(detail=True, methods=['get'])
    def get_saldo(self, request, pk=None):

        try:
            cartao = CartaoCredito.objects.get(pk=pk)
            if cartao.saldo <= 0:
                return Response({"mensagem": "Saldo insuficiente"})
            return Response({"Saldo":cartao.saldo})

        except:
            return Response({"erro": "Cartão não encontrado"}, status=404)

    @action(detail=True, methods=['post'])
    def autorizacao(self, request, pk=None):
        try:
            print("Recebendo requisição...")  # Para verificar se a função está sendo chamada
            cartao = CartaoCredito.objects.get(pk=pk)
            print(f"Cartão encontrado: {cartao.id_cartao}")  # Para confirmar se o cartão foi encontrado

            valor = request.data.get("valor")
            print(f"Valor recebido: {valor}")  # Para verificar o que está chegando na requisição

            if valor is None:
                return Response({"erro": "Informe o valor da transação"}, status=400)


            print(f"Saldo atual: {cartao.saldo}")

            if cartao.saldo is None or cartao.saldo < valor:
                return Response({"mensagem": "Saldo insuficiente"}, status=402)

            cartao.saldo -= valor
            cartao.save()

            print(f"Novo saldo: {cartao.saldo}")

            return Response({"mensagem": "Transação autorizada", "novo_saldo": cartao.saldo}, status=200)

        except CartaoCredito.DoesNotExist:
            return Response({"erro": "Cartão não encontrado"}, status=404)
