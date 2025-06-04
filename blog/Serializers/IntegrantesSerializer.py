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
            'nombre_integrante',
            'semestre', 
            'correo',
            'link_git',
            'imagen',
            'estado',
            'reseña',
            'creador',
            'creador_username'
        ]
        
    def validate_nombre_integrante(self, value):
        """Validar que el nombre no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return value.strip()
    
    def validate_semestre(self, value):
        """Validar que el semestre sea válido."""
        if not value or not value.strip():
            raise serializers.ValidationError("El semestre es requerido.")
        return value.strip()
    
    def validate_correo(self, value):
        """Validar que el correo sea válido."""
        if not value or not value.strip():
            raise serializers.ValidationError("El correo electrónico es requerido.")
        return value.strip().lower()
    
    def validate_link_git(self, value):
        """Validar que el link de GitHub sea válido."""
        if not value or not value.strip():
            raise serializers.ValidationError("El enlace de GitHub es requerido.")
        if not value.startswith('https://github.com/'):
            raise serializers.ValidationError("Debe ser una URL válida de GitHub.")
        return value.strip()
    
    def validate_reseña(self, value):
        """Validar que la reseña no esté vacía."""
        if not value or not value.strip():
            raise serializers.ValidationError("La reseña es requerida.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("La reseña debe tener al menos 10 caracteres.")
        return value.strip()