# 🤝 Guía de Contribución - API_HACK3R

¡Gracias por tu interés en contribuir a API_HACK3R! Esta guía te ayudará a participar en el desarrollo del proyecto.

## 📋 Tabla de Contenidos

- [🚀 Configuración del Entorno de Desarrollo](#-configuración-del-entorno-de-desarrollo)
- [🔧 Proceso de Contribución](#-proceso-de-contribución)
- [📝 Estándares de Código](#-estándares-de-código)
- [🧪 Pruebas](#-pruebas)
- [📚 Documentación](#-documentación)
- [🐛 Reportar Bugs](#-reportar-bugs)
- [💡 Sugerir Nuevas Características](#-sugerir-nuevas-características)
- [❓ Preguntas Frecuentes](#-preguntas-frecuentes)

## 🚀 Configuración del Entorno de Desarrollo

### Prerrequisitos
- Python 3.11 o superior
- PostgreSQL 13+
- Redis (opcional, para Celery)
- Git

### 1. Fork y Clonar el Proyecto

```bash
# Fork el repositorio en GitHub y luego clónalo
git clone https://github.com/TU_USUARIO/API_HACK3R.git
cd API_HACK3R

# Configura el remoto upstream
git remote add upstream https://github.com/MiguelBonilla-sys/API_HACK3R.git
```

### 2. Configurar el Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

```bash
# Crear base de datos PostgreSQL
createdb api_hack3r_dev

# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus configuraciones locales
# DATABASE_URL=postgresql://usuario:password@localhost:5432/api_hack3r_dev
# SECRET_KEY=tu_clave_secreta_para_desarrollo
# DEBUG=True
```

### 4. Ejecutar Migraciones

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Verificar Instalación

```bash
python manage.py runserver
```

Visita `http://localhost:8000/api/docs/` para ver la documentación Swagger.

## 🔧 Proceso de Contribución

### 1. Crear una Rama de Trabajo

```bash
# Actualizar rama principal
git checkout main
git pull upstream main

# Crear nueva rama
git checkout -b feature/mi-nueva-caracteristica
# o
git checkout -b fix/correccion-de-bug
```

### 2. Hacer Cambios

- Realiza los cambios necesarios
- Sigue los estándares de código
- Escribe tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 3. Confirmar Cambios

```bash
# Agregar archivos modificados
git add .

# Commit con mensaje descriptivo
git commit -m "feat: añadir endpoint para estadísticas de cursos"
```

### 4. Push y Pull Request

```bash
# Subir cambios a tu fork
git push origin feature/mi-nueva-caracteristica

# Crear Pull Request en GitHub
```

### Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formateo de código
- `refactor:` Refactorización
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento

Ejemplos:
```
feat: añadir filtro por fecha en endpoint de noticias
fix: corregir error en serialización de proyectos
docs: actualizar README con nuevos endpoints
test: añadir tests para modelo de conferencias
```

## 📝 Estándares de Código

### Python/Django

#### Estilo de Código
- Seguir [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usar [Black](https://github.com/psf/black) para formateo automático
- Longitud máxima de línea: 88 caracteres

#### Estructura de Archivos
```python
# Orden de imports
import os
import sys
from pathlib import Path

from django.db import models
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from .models import MiModelo
```

#### Nomenclatura
- **Clases**: `PascalCase` (ej: `ConferenciasViewSet`)
- **Funciones/métodos**: `snake_case` (ej: `get_user_profile`)
- **Variables**: `snake_case` (ej: `user_data`)
- **Constantes**: `UPPER_CASE` (ej: `MAX_UPLOAD_SIZE`)

### Django REST Framework

#### ViewSets
```python
class ConferenciasViewSet(ModelViewSet):
    """
    ViewSet para gestionar conferencias académicas.
    
    Proporciona operaciones CRUD completas y endpoints personalizados
    para la gestión de conferencias.
    """
    queryset = Conferencias.objects.all()
    serializer_class = ConferenciasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['fecha_conferencia', 'ponente_conferencia']
    search_fields = ['nombre_conferencia', 'descripcion_conferencia']
    ordering_fields = ['fecha_conferencia', 'nombre_conferencia']
    
    @action(detail=False, methods=['get'])
    def proximas(self, request):
        """Obtener conferencias próximas."""
        # Implementación...
```

#### Serializers
```python
class ConferenciasSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Conferencias."""
    
    class Meta:
        model = Conferencias
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_fecha_conferencia(self, value):
        """Validar que la fecha sea futura."""
        if value < timezone.now():
            raise serializers.ValidationError(
                "La fecha debe ser futura."
            )
        return value
```

#### Modelos
```python
class Conferencias(models.Model):
    """
    Modelo para gestionar conferencias académicas.
    
    Attributes:
        nombre_conferencia (str): Nombre de la conferencia
        fecha_conferencia (datetime): Fecha y hora del evento
        ponente_conferencia (str): Nombre del ponente
        descripcion_conferencia (str): Descripción del evento
    """
    
    nombre_conferencia = models.CharField(
        max_length=850,
        help_text="Nombre descriptivo de la conferencia"
    )
    fecha_conferencia = models.DateTimeField(
        help_text="Fecha y hora de la conferencia"
    )
    # ... más campos
    
    class Meta:
        verbose_name = "Conferencia"
        verbose_name_plural = "Conferencias"
        ordering = ['-fecha_conferencia']
    
    def __str__(self):
        return self.nombre_conferencia
```

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas específicas
python manage.py test blog.tests.test_models

# Ejecutar con coverage
coverage run --source='.' manage.py test
coverage report
```

### Escribir Pruebas

#### Pruebas de Modelos
```python
from django.test import TestCase
from django.contrib.auth.models import User
from blog.Models.ConferenciasModel import Conferencias

class ConferenciasModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_crear_conferencia(self):
        """Test crear una nueva conferencia."""
        conferencia = Conferencias.objects.create(
            nombre_conferencia='Test Conference',
            fecha_conferencia='2024-12-25T10:00:00Z',
            ponente_conferencia='Dr. Test',
            descripcion_conferencia='Test description',
            creador=self.user
        )
        
        self.assertEqual(conferencia.nombre_conferencia, 'Test Conference')
        self.assertEqual(str(conferencia), 'Test Conference')
```

#### Pruebas de API
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class ConferenciasAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_crear_conferencia(self):
        """Test crear conferencia vía API."""
        url = reverse('conferencias-list')
        data = {
            'nombre_conferencia': 'Nueva Conferencia',
            'fecha_conferencia': '2024-12-25T10:00:00Z',
            'ponente_conferencia': 'Dr. Ejemplo',
            'descripcion_conferencia': 'Descripción de prueba'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## 📚 Documentación

### Docstrings

Usa docstrings en formato Google:

```python
def calculate_duration(start_date, end_date):
    """
    Calcula la duración entre dos fechas.
    
    Args:
        start_date (datetime): Fecha de inicio
        end_date (datetime): Fecha de finalización
    
    Returns:
        int: Duración en días
    
    Raises:
        ValueError: Si end_date es anterior a start_date
    """
    if end_date < start_date:
        raise ValueError("La fecha final debe ser posterior a la inicial")
    
    return (end_date - start_date).days
```

### Documentación API

- Actualiza la documentación Swagger cuando agregues nuevos endpoints
- Documenta parámetros y respuestas esperadas
- Incluye ejemplos de uso

## 🐛 Reportar Bugs

### Antes de Reportar
1. Busca en [issues existentes](https://github.com/MiguelBonilla-sys/API_HACK3R/issues)
2. Verifica que sea un bug reproducible
3. Prueba en la última versión del código

### Información a Incluir
- **Descripción**: Explica el problema claramente
- **Pasos para reproducir**: Lista exacta de pasos
- **Comportamiento esperado**: Qué debería pasar
- **Comportamiento actual**: Qué está pasando
- **Entorno**: SO, versión de Python, etc.
- **Logs**: Incluye mensajes de error relevantes

### Plantilla de Bug Report
```markdown
## Descripción del Bug
Una descripción clara del problema.

## Pasos para Reproducir
1. Ir a '...'
2. Hacer click en '...'
3. Observar el error

## Comportamiento Esperado
Descripción de lo que debería pasar.

## Comportamiento Actual
Descripción de lo que está pasando.

## Entorno
- OS: [ej. Ubuntu 20.04]
- Python: [ej. 3.11.2]
- Django: [ej. 5.1.5]

## Logs
```
Logs relevantes aquí
```
```

## 💡 Sugerir Nuevas Características

### Antes de Sugerir
1. Busca en [issues existentes](https://github.com/MiguelBonilla-sys/API_HACK3R/issues)
2. Considera si encaja con la visión del proyecto
3. Piensa en la implementación general

### Información a Incluir
- **Descripción**: Explica la funcionalidad deseada
- **Motivación**: Por qué es necesaria esta característica
- **Implementación**: Ideas sobre cómo implementarla
- **Alternativas**: Otras soluciones consideradas

### Plantilla de Feature Request
```markdown
## Resumen de la Característica
Descripción breve de la funcionalidad.

## Motivación
¿Por qué es necesaria esta característica?

## Descripción Detallada
Explicación completa de la funcionalidad.

## Implementación Propuesta
Ideas sobre cómo implementar la característica.

## Alternativas Consideradas
Otras soluciones que has considerado.
```

## ❓ Preguntas Frecuentes

### ¿Cómo configuro Cloudinary para desarrollo?
1. Crea una cuenta en [Cloudinary](https://cloudinary.com/)
2. Obtén tus credenciales del dashboard
3. Configura las variables en tu archivo `.env`

### ¿Necesito Redis para desarrollo?
No es obligatorio. Redis se usa para Celery (tareas asíncronas), pero puedes desarrollar sin él.

### ¿Cómo contribuyo a la documentación?
1. Actualiza los docstrings en el código
2. Modifica el README.md si es necesario
3. Agrega ejemplos de uso

### ¿Puedo usar Docker?
Sí, aunque no está incluido en el repositorio, puedes crear un `Dockerfile` para tu entorno de desarrollo.

### ¿Qué branches debo usar?
- `main`: Código de producción
- `develop`: Rama de desarrollo (si existe)
- `feature/nombre`: Para nuevas características
- `fix/nombre`: Para correcciones de bugs

## 📞 Contacto

### Canales de Comunicación
- **GitHub Issues**: Para bugs y feature requests
- **GitHub Discussions**: Para preguntas generales
- **Email**: Disponible en el perfil de GitHub del autor

### Mantenedores
- **Miguel Bonilla** (@MiguelBonilla-sys) - Autor principal

---

**¡Gracias por contribuir a API_HACK3R!** 🚀

Tu participación ayuda a mejorar esta herramienta para toda la comunidad académica.