from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from enderecos.models import Endereco, TipoEndereco 
from enderecos.serializers import EnderecoSerializer, TipoEnderecoSerializer

# Create your views here.
class EnderecoViewSet(ModelViewSet):    
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class TipoEnderecoViewSet(ModelViewSet):    
    queryset = TipoEndereco.objects.all()
    serializer_class = TipoEnderecoSerializer
