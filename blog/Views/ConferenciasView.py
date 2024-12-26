from rest_framework import viewsets
from blog.Models.ConferenciasModel import Conferencias
from blog.Serializers.ConferenciasSerializer import ConferenciasSerializer

class ConferenciasViewSet(viewsets.ModelViewSet):
    serializer_class = ConferenciasSerializer
    queryset = Conferencias.objects.all()