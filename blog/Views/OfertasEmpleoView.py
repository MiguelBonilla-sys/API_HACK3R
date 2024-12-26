from rest_framework import viewsets
from blog.Models.OfertasEmpleoModel import OfertasEmpleo
from blog.Serializers.OfertasSerializer import OfertasEmpleoSerializer

class OfertasEmpleoViewSet(viewsets.ModelViewSet):
    serializer_class = OfertasEmpleoSerializer
    queryset = OfertasEmpleo.objects.all()