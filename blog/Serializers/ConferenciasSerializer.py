from rest_framework import serializers
from blog.Models.ConferenciasModel import Conferencias
from django.contrib.auth.models import User

class ConferenciasSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Conferencias con soporte completo para Cloudinary.
    """
    # Campo de imagen como ImageField para subida de archivos
    imagen_conferencia = serializers.ImageField(required=False, allow_null=True)
    
    # Campos de solo lectura
    creador = serializers.PrimaryKeyRelatedField(read_only=True)
    creador_username = serializers.CharField(source='creador.username', read_only=True)
    idconferencia = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conferencias
        fields = [
            'idconferencia',
            'nombre_conferencia',
            'ponente_conferencia',
            'fecha_conferencia',
            'descripcion_conferencia',
            'imagen_conferencia',
            'link_conferencia',
            'creador',
            'creador_username'
        ]
        
    def validate_nombre_conferencia(self, value):
        """Validar que el nombre de la conferencia no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la conferencia no puede estar vacío.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El nombre debe tener al menos 5 caracteres.")
        return value.strip()
    
    def validate_ponente_conferencia(self, value):
        """Validar que el ponente no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del ponente es requerido.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre del ponente debe tener al menos 2 caracteres.")
        return value.strip()
    
    def validate_descripcion_conferencia(self, value):
        """Validar que la descripción no esté vacía."""
        if not value or not value.strip():
            raise serializers.ValidationError("La descripción de la conferencia es requerida.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return value.strip()
    
    def validate_link_conferencia(self, value):
        """Validar que el link sea una URL válida."""
        if not value or not value.strip():
            raise serializers.ValidationError("El link de la conferencia es requerido.")
        return value.strip()