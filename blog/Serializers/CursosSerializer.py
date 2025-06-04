from rest_framework import serializers
from blog.Models.CursosModel import Cursos
from django.contrib.auth.models import User
from django.utils import timezone

# Convierte el modelo Cursos(Python) en un JSON para ser
# Consumido por la API 
class CursosSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cursos con validaciones completas.
    """
    # Campos de solo lectura
    creador = serializers.PrimaryKeyRelatedField(read_only=True)
    creador_username = serializers.CharField(source='creador.username', read_only=True)
    idcursos = serializers.IntegerField(read_only=True)
    
    # Campos calculados
    is_active = serializers.BooleanField(read_only=True)
    duration_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cursos
        fields = [
            'idcursos',
            'nombre_curso',
            'fechainicial_curso',
            'fechafinal_curso',
            'link_curso',
            'descripcion_curso',
            'creador',
            'creador_username',
            'is_active',
            'duration_days'
        ]
        
    def validate_nombre_curso(self, value):
        """Validar que el nombre del curso no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del curso no puede estar vacío.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El nombre del curso debe tener al menos 5 caracteres.")
        return value.strip()
    
    def validate_descripcion_curso(self, value):
        """Validar que la descripción no esté vacía."""
        if not value or not value.strip():
            raise serializers.ValidationError("La descripción del curso es requerida.")
        if len(value.strip()) < 20:
            raise serializers.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return value.strip()
    
    def validate_link_curso(self, value):
        """Validar que el link sea una URL válida."""
        if not value or not value.strip():
            raise serializers.ValidationError("El link del curso es requerido.")
        return value.strip()
    
    def validate(self, data):
        """Validaciones a nivel de objeto."""
        fechainicial = data.get('fechainicial_curso')
        fechafinal = data.get('fechafinal_curso')
        
        if fechainicial and fechafinal:
            if fechainicial >= fechafinal:
                raise serializers.ValidationError({
                    'fechafinal_curso': 'La fecha final debe ser posterior a la fecha inicial.'
                })
            
            # Validar que las fechas no sean muy antiguas
            if fechainicial < timezone.now() - timezone.timedelta(days=365*2):
                raise serializers.ValidationError({
                    'fechainicial_curso': 'La fecha inicial no puede ser anterior a 2 años.'
                })
        
        return data