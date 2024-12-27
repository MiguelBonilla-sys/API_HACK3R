from rest_framework import serializers
from blog.Models.ConferenciasModel import Conferencias

class ConferenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conferencias
        fields = '__all__'