from rest_framework import serializers
from blog.Models.IntegrantesModel import Integrantes
from django.contrib.auth.models import User

# Convierte el modelo Integrantes(Python) en un JSON para ser
# Consumido por la API
class IntegrantesSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Integrantes con soporte completo para Cloudinary.
    """
    # Campo de imagen como ImageField para subida de archivos
    imagen = serializers.ImageField(required=False, allow_null=True)
    
    # Campos de solo lectura
    creador = serializers.PrimaryKeyRelatedField(read_only=True)
    creador_username = serializers.CharField(source='creador.username', read_only=True)
    idintegrantes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Integrantes
        fields = [
            'idintegrantes',
            'nombres',
            'apellidos', 
            'celular',
            'correo',
            'linkgithub',
            'linklinkedin',
            'linkinstagram',
            'linktwitter',
            'imagen',
            'estado',
            'creador',
            'creador_username'
        ]
        
    def validate_nombres(self, value):
        """Validar que el nombre no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return value.strip()
    
    def validate_apellidos(self, value):
        """Validar que los apellidos no estén vacíos."""
        if not value or not value.strip():
            raise serializers.ValidationError("Los apellidos no pueden estar vacíos.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Los apellidos deben tener al menos 2 caracteres.")
        return value.strip()
    
    def validate_correo(self, value):
        """Validar que el correo sea válido."""
        if not value or not value.strip():
            raise serializers.ValidationError("El correo electrónico es requerido.")
        return value.strip().lower()