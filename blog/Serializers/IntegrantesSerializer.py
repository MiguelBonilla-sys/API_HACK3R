from rest_framework import serializers
from blog.Models.IntegrantesModel import Integrantes
import base64
import binascii
# Convierte el modelo Integrantes(Python) en un JSON para ser
# Consumido por la API
class IntegrantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integrantes
        fields = '__all__'
        
    def validate_imagen_integrante(self, value):
        if not value.startswith('data:image/'):
            raise serializers.ValidationError('La imagen debe estar en formato base64')
        try:
            # Verificar que sea un base64 válido
            formato, imgstr = value.split(';base64,')
            base64.b64decode(imgstr)
        except binascii.Error:
            raise serializers.ValidationError('La imagen no es un base64 válido')
        return value