from rest_framework import serializers
from blog.Models.OfertasEmpleoModel import OfertasEmpleo
from django.contrib.auth.models import User

class OfertasEmpleoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo OfertasEmpleo con soporte completo para Cloudinary.
    """
    # Campo de imagen como ImageField para subida de archivos
    imagen = serializers.ImageField(required=False, allow_null=True)
    
    # Campos de solo lectura
    creador = serializers.PrimaryKeyRelatedField(read_only=True)
    creador_username = serializers.CharField(source='creador.username', read_only=True)
    idoferta = serializers.IntegerField(read_only=True)
    fecha_publicacion = serializers.DateTimeField(read_only=True)
    
    # Campo calculado
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = OfertasEmpleo
        fields = [
            'idoferta',
            'titulo_empleo',
            'empresa',
            'descripcion_empleo',
            'fecha_publicacion',
            'fecha_expiracion',
            'imagen',
            'link_oferta',
            'creador',
            'creador_username',
            'is_expired'
        ]
        
    def validate_titulo_empleo(self, value):
        """Validar que el título no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El título de la oferta no puede estar vacío.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value.strip()
    
    def validate_empresa(self, value):
        """Validar que la empresa no esté vacía."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la empresa es requerido.")
        return value.strip()
    
    def validate_descripcion_empleo(self, value):
        """Validar que la descripción no esté vacía."""
        if not value or not value.strip():
            raise serializers.ValidationError("La descripción de la oferta es requerida.")
        if len(value.strip()) < 20:
            raise serializers.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return value.strip()
    
    def validate_link_oferta(self, value):
        """Validar que el link sea una URL válida."""
        if not value or not value.strip():
            raise serializers.ValidationError("El link de la oferta es requerido.")
        return value.strip()