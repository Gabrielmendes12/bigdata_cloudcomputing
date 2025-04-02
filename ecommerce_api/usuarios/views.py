from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer


# Create your views here.
class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer