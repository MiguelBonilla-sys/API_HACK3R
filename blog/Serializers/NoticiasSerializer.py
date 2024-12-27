from rest_framework import serializers
from blog.Models.NoticiasModel import Noticias
# Convierte el modelo Noticias(Python) en un JSON para ser
# Consumido por la API
class NoticiasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticias
        fields = '__all__'