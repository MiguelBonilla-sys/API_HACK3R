from rest_framework import viewsets
from blog.Models.IntegrantesModel import Integrantes
from blog.Serializers.IntegrantesSerializer import IntegrantesSerializer

class IntegrantesViewSet(viewsets.ModelViewSet):
    serializer_class = IntegrantesSerializer
    queryset = Integrantes.objects.all()