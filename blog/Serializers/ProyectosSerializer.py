from rest_framework import serializers
from blog.Models.ProyectosModel import Proyectos
from blog.Models.IntegrantesModel import Integrantes
from django.contrib.auth.models import User
from django.utils import timezone

# Convierte el modelo Proyectos(Python) en un JSON para ser
# Consumido por la API
class ProyectosSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Proyectos con validaciones completas.
    """
    # Campos de solo lectura
    creador = serializers.PrimaryKeyRelatedField(read_only=True)
    creador_username = serializers.CharField(source='creador.username', read_only=True)
    idproyectos = serializers.IntegerField(read_only=True)
    
    # Campos calculados
    total_integrantes = serializers.IntegerField(read_only=True)
    is_recent = serializers.BooleanField(read_only=True)
    
    # Relación ManyToMany con integrantes
    integrantes = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Integrantes.objects.filter(estado=True),
        required=False
    )
    
    # Campo adicional para mostrar información de integrantes
    integrantes_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Proyectos
        fields = [
            'idproyectos',
            'nombre_proyecto',
            'fecha_proyecto',
            'link_proyecto',
            'description_proyecto',
            'creador',
            'creador_username',
            'integrantes',
            'integrantes_info',
            'total_integrantes',
            'is_recent'
        ]
        
    def get_integrantes_info(self, obj):
        """Obtener información básica de los integrantes del proyecto."""
        try:
            integrantes = obj.get_integrantes_activos()
            return [
                {
                    'id': integrante.idintegrantes,
                    'nombre_completo': f"{integrante.nombres} {integrante.apellidos}",
                    'correo': integrante.correo
                }
                for integrante in integrantes
            ]
        except:
            return []
        
    def validate_nombre_proyecto(self, value):
        """Validar que el nombre del proyecto no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del proyecto no puede estar vacío.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El nombre del proyecto debe tener al menos 5 caracteres.")
        return value.strip()
    
    def validate_description_proyecto(self, value):
        """Validar que la descripción no esté vacía."""
        if not value or not value.strip():
            raise serializers.ValidationError("La descripción del proyecto es requerida.")
        if len(value.strip()) < 20:
            raise serializers.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return value.strip()
    
    def validate_link_proyecto(self, value):
        """Validar que el link sea una URL válida."""
        if not value or not value.strip():
            raise serializers.ValidationError("El link del proyecto es requerido.")
        return value.strip()
    
    def validate_fecha_proyecto(self, value):
        """Validar que la fecha del proyecto sea razonable."""
        if value:
            # No permitir fechas muy futuras (más de 1 año)
            if value > timezone.now() + timezone.timedelta(days=365):
                raise serializers.ValidationError("La fecha del proyecto no puede ser más de 1 año en el futuro.")
            
            # No permitir fechas muy antiguas (más de 5 años)
            if value < timezone.now() - timezone.timedelta(days=365*5):
                raise serializers.ValidationError("La fecha del proyecto no puede ser anterior a 5 años.")
        
        return value
    
    def create(self, validated_data):
        """Crear proyecto con manejo de integrantes."""
        integrantes_data = validated_data.pop('integrantes', [])
        proyecto = Proyectos.objects.create(**validated_data)
        
        # Asignar integrantes si se proporcionaron
        if integrantes_data:
            proyecto.integrantes.set(integrantes_data)
        
        return proyecto
    
    def update(self, instance, validated_data):
        """Actualizar proyecto con manejo de integrantes."""
        integrantes_data = validated_data.pop('integrantes', None)
        
        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar integrantes si se proporcionaron
        if integrantes_data is not None:
            instance.integrantes.set(integrantes_data)
        
        return instance