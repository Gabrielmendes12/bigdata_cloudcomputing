from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
from enderecos.serializers import EnderecoSerializer
from enderecos.models import Endereco
from cartoes.models import CartaoCredito
from cartoes.serializers import CartaoCreditoSerializer


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    # POST /usuarios/<id>/endereco/
    @action(detail=True, methods=['post'], url_path='endereco')
    def adicionar_endereco(self, request, pk=None):
        usuario = self.get_object()
        data = request.data.copy()
        data['usuario'] = usuario.id
        serializer = EnderecoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET /usuarios/<id>/enderecos/
    @action(detail=True, methods=['get'], url_path='enderecos')
    def listar_enderecos(self, request, pk=None):
        usuario = self.get_object()
        enderecos = Endereco.objects.filter(usuario=usuario)
        serializer = EnderecoSerializer(enderecos, many=True)
        return Response(serializer.data)

    # POST /usuarios/<id>/cartao/
    @action(detail=True, methods=['post'], url_path='cartao')
    def adicionar_cartao(self, request, pk=None):
        usuario = self.get_object()
        data = request.data.copy()
        data['usuario'] = usuario.id
        serializer = CartaoCreditoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET /usuarios/<id>/cartoes/
    @action(detail=True, methods=['get'], url_path='cartoes')
    def listar_cartoes(self, request, pk=None):
        usuario = self.get_object()
        cartoes = CartaoCredito.objects.filter(usuario=usuario)
        serializer = CartaoCreditoSerializer(cartoes, many=True)
        return Response(serializer.data)
