from rest_framework import viewsets
from blog.Models.ProyectosModel import Proyectos
from blog.Serializers.ProyectosSerializer import ProyectosSerializer

class ProyectosViewSet(viewsets.ModelViewSet):
    serializer_class = ProyectosSerializer
    queryset = Proyectos.objects.all()