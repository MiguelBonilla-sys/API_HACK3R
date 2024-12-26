from rest_framework import viewsets
from blog.Models.NoticiasModel import Noticias
from blog.Serializers.NoticiasSerializer import NoticiasSerializer

class NoticiasViewSet(viewsets.ModelViewSet):
    serializer_class = NoticiasSerializer
    queryset = Noticias.objects.all()