from rest_framework import serializers
from blog.Models.NoticiasModel import Noticias
from django.contrib.auth.models import User

class NoticiasSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Noticias con soporte completo para Cloudinary.
    """
    # Campo de imagen como ImageField para subida de archivos
    imagen_noticia = serializers.ImageField(required=False, allow_null=True)
    
    # Campos de solo lectura
    creador = serializers.PrimaryKeyRelatedField(read_only=True)
    creador_username = serializers.CharField(source='creador.username', read_only=True)
    fecha_noticia = serializers.DateTimeField(read_only=True)
    idnoticia = serializers.IntegerField(read_only=True)
    
    # Campos calculados
    is_recent = serializers.BooleanField(read_only=True)
    summary = serializers.CharField(read_only=True)

    class Meta:
        model = Noticias
        fields = [
            'idnoticia',
            'nombre_noticia', 
            'fecha_noticia',
            'link_noticia',
            'description_noticia',
            'creador',
            'creador_username',
            'fuente',
            'imagen_noticia',
            'is_recent',
            'summary'
        ]
        
    def validate_nombre_noticia(self, value):
        """Validar que el título no esté vacío y tenga una longitud adecuada."""
        if not value or not value.strip():
            raise serializers.ValidationError("El título de la noticia no puede estar vacío.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("El título debe tener al menos 10 caracteres.")
        return value.strip()
    
    def validate_description_noticia(self, value):
        """Validar que la descripción no esté vacía."""
        if not value or not value.strip():
            raise serializers.ValidationError("La descripción no puede estar vacía.")
        if len(value.strip()) < 20:
            raise serializers.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return value.strip()
    
    def validate_link_noticia(self, value):
        """Validar que el link sea una URL válida."""
        if not value or not value.strip():
            raise serializers.ValidationError("El link de la noticia es requerido.")
        return value.strip()