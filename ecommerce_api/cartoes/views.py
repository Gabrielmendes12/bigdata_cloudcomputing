from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from cartoes.models import CartaoCredito
from cartoes.serializers import CartaoCreditoSerializer

# Create your views here.
class CartaoCreditoViewSet(ModelViewSet):
    queryset = CartaoCredito.objects.all()
    serializer_class = CartaoCreditoSerializer

