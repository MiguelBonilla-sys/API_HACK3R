from rest_framework import viewsets
from blog.Models.CursosModel import Cursos
from blog.Serializers.CursosSerializer import CursosSerializer

class CursosViewSet(viewsets.ModelViewSet):
    serializer_class = CursosSerializer
    queryset = Cursos.objects.all()