# 🚀 API_HACK3R - Sistema de Gestión Académica

**API REST completa en Django para gestión académica - Conferencias, Cursos, Integrantes, Noticias, Ofertas de Empleo y Proyectos. Desplegada en Railway con autenticación, AuditLog y documentación Swagger.**

[![Estado](https://img.shields.io/badge/Estado-Funcional-brightgreen)](https://apihack3r-production.up.railway.app)
[![Django](https://img.shields.io/badge/Django-5.1.5-092E20?logo=django)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-ff1709)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)](https://www.postgresql.org/)
[![Railway](https://img.shields.io/badge/Deployed-Railway-0B0D0E?logo=railway)](https://railway.app/)

## 🌐 Enlaces de Producción

- **🌐 Aplicación**: https://apihack3r-production.up.railway.app
- **🔐 Panel de Administración**: https://apihack3r-production.up.railway.app/admin/
- **📚 Documentación API (Swagger)**: https://apihack3r-production.up.railway.app/api/swagger/
- **🚀 API Base URL**: https://apihack3r-production.up.railway.app/api/

## 📋 Descripción del Proyecto

API_HACK3R es un sistema completo de gestión académica desarrollado como API REST que permite administrar:

- 📚 **Conferencias** académicas y eventos
- 🎓 **Cursos** y programas educativos  
- 👥 **Integrantes** del equipo/organización
- 📰 **Noticias** y actualizaciones
- 💼 **Ofertas de empleo** para estudiantes
- 🚀 **Proyectos** académicos y de investigación
- 📊 **Sistema de auditoría** completo

## ✨ Características Principales

### 🔐 Sistema de Autenticación Completo
- ✅ Registro y login de usuarios
- ✅ Autenticación por Token
- ✅ Perfiles de usuario personalizados
- ✅ Sistema de permisos (Admin/Staff/User)
- ✅ Endpoints de gestión de perfiles

### 🚀 API Robusta y Versionada
- ✅ Endpoints RESTful completos (CRUD)
- ✅ Filtros y búsquedas avanzadas
- ✅ Paginación automática
- ✅ Validación de datos robusta
- ✅ Documentación automática con Swagger

### 📊 Funcionalidades Avanzadas
- ✅ Sistema de AuditLog para seguimiento
- ✅ Dashboard diferenciado por roles
- ✅ Estadísticas y reportes personalizados
- ✅ Limpieza automática de datos expirados
- ✅ Manejo de relaciones Many-to-Many
- ✅ Almacenamiento en la nube (Cloudinary)

## 🏗️ Arquitectura Técnica

### Stack Tecnológico
- **Backend**: Django 5.1.5 + Django REST Framework 3.15.2
- **Base de Datos**: PostgreSQL
- **Autenticación**: dj-rest-auth + Token Authentication
- **Almacenamiento**: Cloudinary para imágenes
- **Documentación**: drf-yasg (Swagger/OpenAPI)
- **Despliegue**: Railway
- **Cache/Cola**: Redis + Celery

### Dependencias Principales
```
Django==5.1.5
djangorestframework==3.15.2
dj-rest-auth==7.0.1
django-allauth==65.8.1
django-filter==25.1
django-cors-headers==4.6.0
drf-yasg==1.21.8
psycopg2-binary==2.9.10
cloudinary==1.41.0
celery==5.4.0
redis==5.0.1
gunicorn==21.2.0
```

## 🚀 Endpoints Principales

### 📊 API Base
```
GET /api/                           # Vista raíz con todos los endpoints
```

### 🔐 Autenticación
```
POST /auth/registration/            # Registro de usuario
POST /auth/login/                   # Inicio de sesión
POST /auth/logout/                  # Cerrar sesión
GET  /auth/user/                    # Información del usuario
GET  /api/profile/                  # Perfil personalizado
PUT  /api/profile/update/           # Actualizar perfil
```

### 📚 Conferencias
```
GET    /api/conferencias/                    # Lista todas las conferencias
POST   /api/conferencias/                    # Crear nueva conferencia
GET    /api/conferencias/{id}/               # Detalle de conferencia
PUT    /api/conferencias/{id}/               # Actualizar conferencia
DELETE /api/conferencias/{id}/               # Eliminar conferencia
GET    /api/conferencias/proximas/           # Conferencias próximas
```

### 🎓 Cursos
```
GET    /api/cursos/                          # Lista todos los cursos
POST   /api/cursos/                          # Crear nuevo curso
GET    /api/cursos/{id}/                     # Detalle de curso
PUT    /api/cursos/{id}/                     # Actualizar curso
DELETE /api/cursos/{id}/                     # Eliminar curso
GET    /api/cursos/activos/                  # Cursos activos
```

### 👥 Integrantes
```
GET    /api/integrantes/                     # Lista todos los integrantes
POST   /api/integrantes/                     # Crear nuevo integrante
GET    /api/integrantes/{id}/                # Detalle de integrante
PUT    /api/integrantes/{id}/                # Actualizar integrante
DELETE /api/integrantes/{id}/                # Eliminar integrante
```

### 📰 Noticias
```
GET    /api/noticias/                        # Lista todas las noticias
POST   /api/noticias/                        # Crear nueva noticia
GET    /api/noticias/{id}/                   # Detalle de noticia
PUT    /api/noticias/{id}/                   # Actualizar noticia
DELETE /api/noticias/{id}/                   # Eliminar noticia
GET    /api/noticias/recientes/              # Noticias recientes
```

### 💼 Ofertas de Empleo
```
GET    /api/ofertasempleo/                   # Lista todas las ofertas
POST   /api/ofertasempleo/                   # Crear nueva oferta
GET    /api/ofertasempleo/{id}/              # Detalle de oferta
PUT    /api/ofertasempleo/{id}/              # Actualizar oferta
DELETE /api/ofertasempleo/{id}/              # Eliminar oferta
```

### 🚀 Proyectos
```
GET    /api/proyectos/                       # Lista todos los proyectos
POST   /api/proyectos/                       # Crear nuevo proyecto
GET    /api/proyectos/{id}/                  # Detalle de proyecto
PUT    /api/proyectos/{id}/                  # Actualizar proyecto
DELETE /api/proyectos/{id}/                  # Eliminar proyecto
```

### 📊 Sistema de Auditoría (Solo Admin)
```
GET    /api/auditlog/                        # Lista de logs de auditoría
GET    /api/auditlog/{id}/                   # Detalle de log específico
GET    /api/auditlog/resumen_actividad/      # Estadísticas 24h/7d
GET    /api/auditlog/errores_recientes/      # Logs de error
POST   /api/auditlog/limpiar_logs_antiguos/  # Limpieza (superuser)
```

## 🔧 Instalación y Configuración Local

### Prerrequisitos
- Python 3.11+
- PostgreSQL 13+
- Redis (opcional, para Celery)
- Git

### 1. Clonar el Repositorio
```bash
git clone https://github.com/MiguelBonilla-sys/API_HACK3R.git
cd API_HACK3R
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
# Configuración de Django
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui
DEBUG=True

# Base de datos PostgreSQL
DATABASE_URL=postgresql://usuario:password@localhost:5432/api_hack3r

# Cloudinary (para archivos)
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# Redis (opcional)
REDIS_URL=redis://localhost:6379/0
```

### 5. Configurar Base de Datos
```bash
# Crear base de datos PostgreSQL
createdb api_hack3r

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 6. Ejecutar el Servidor
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/`

## 📝 Ejemplos de Uso

### Autenticación

#### Registro de Usuario
```bash
curl -X POST http://localhost:8000/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "usuario@example.com",
    "password1": "contraseña_segura123",
    "password2": "contraseña_segura123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "password": "contraseña_segura123"
  }'
```

Respuesta:
```json
{
  "key": "token_de_autenticacion_aqui"
}
```

### Operaciones CRUD

#### Crear una Conferencia
```bash
curl -X POST http://localhost:8000/api/conferencias/ \
  -H "Authorization: Token tu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_conferencia": "Inteligencia Artificial en 2024",
    "ponente_conferencia": "Dr. Juan Pérez",
    "fecha_conferencia": "2024-12-15T10:00:00Z",
    "descripcion_conferencia": "Conferencia sobre las últimas tendencias en IA",
    "link_conferencia": "https://example.com/conferencia"
  }'
```

#### Obtener Lista de Cursos
```bash
curl -X GET http://localhost:8000/api/cursos/ \
  -H "Authorization: Token tu_token_aqui"
```

#### Filtrar Noticias Recientes
```bash
curl -X GET http://localhost:8000/api/noticias/recientes/ \
  -H "Authorization: Token tu_token_aqui"
```

### Filtros y Búsquedas

#### Buscar Conferencias por Ponente
```bash
curl -X GET "http://localhost:8000/api/conferencias/?search=Dr.%20Juan" \
  -H "Authorization: Token tu_token_aqui"
```

#### Filtrar Cursos por Fecha
```bash
curl -X GET "http://localhost:8000/api/cursos/?fechainicial_curso__gte=2024-01-01" \
  -H "Authorization: Token tu_token_aqui"
```

#### Ordenar Proyectos por Fecha
```bash
curl -X GET "http://localhost:8000/api/proyectos/?ordering=-fecha_proyecto" \
  -H "Authorization: Token tu_token_aqui"
```

## 🔐 Autenticación y Permisos

### Tipos de Usuario
- **Superuser**: Acceso completo a todo el sistema
- **Staff**: Acceso al panel de administración
- **User**: Acceso a endpoints públicos y operaciones básicas

### Endpoints Protegidos
- **AuditLog**: Solo admins pueden acceder
- **Operaciones CRUD**: Requieren autenticación
- **Información de perfil**: Solo el usuario propietario

### Headers de Autenticación
```http
Authorization: Token tu_token_de_autenticacion_aqui
```

## 📊 Sistema de Auditoría

El sistema incluye un completo sistema de auditoría que registra:
- Operaciones CRUD en todos los modelos
- Cambios en perfiles de usuario
- Intentos de acceso no autorizados
- Errores del sistema

### Acceso a Logs (Solo Admin)
```bash
curl -X GET http://localhost:8000/api/auditlog/ \
  -H "Authorization: Token token_de_admin"
```

### Estadísticas de Actividad
```bash
curl -X GET http://localhost:8000/api/auditlog/resumen_actividad/ \
  -H "Authorization: Token token_de_admin"
```

## 🚀 Despliegue en Producción

### Railway (Actual)
El proyecto está desplegado en Railway con:
- PostgreSQL automático
- Variables de entorno configuradas
- SSL/HTTPS habilitado
- Dominio personalizado

### Variables de Entorno en Producción
```env
SECRET_KEY=clave_secreta_produccion
DEBUG=False
ALLOWED_HOSTS=*.railway.app,tu-dominio.com
DATABASE_URL=postgresql://... (auto-generada)
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
RAILWAY_ENVIRONMENT=production
```

### Comandos Post-Despliegue
```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

## 📁 Estructura del Proyecto

```
API_HACK3R/
├── blog/                          # Aplicación principal
│   ├── Models/                    # Modelos de datos
│   │   ├── ConferenciasModel.py   # Modelo de conferencias
│   │   ├── CursosModel.py         # Modelo de cursos
│   │   ├── IntegrantesModel.py    # Modelo de integrantes
│   │   ├── NoticiasModel.py       # Modelo de noticias
│   │   ├── OfertasEmpleoModel.py  # Modelo de ofertas de empleo
│   │   ├── ProyectosModel.py      # Modelo de proyectos
│   │   └── AuditLogModel.py       # Modelo de auditoría
│   ├── Views/                     # Vistas y ViewSets
│   │   ├── ConferenciasView.py    # CRUD de conferencias
│   │   ├── CursosView.py          # CRUD de cursos
│   │   ├── IntegrantesView.py     # CRUD de integrantes
│   │   ├── NoticiasView.py        # CRUD de noticias
│   │   ├── OfertasEmpleoView.py   # CRUD de ofertas
│   │   ├── ProyectosView.py       # CRUD de proyectos
│   │   ├── AuditLogView.py        # Vistas de auditoría
│   │   └── AuthView.py            # Vistas de autenticación
│   ├── Serializers/               # Serializadores DRF
│   ├── management/                # Comandos de gestión
│   ├── filters.py                 # Filtros personalizados
│   ├── pagination.py              # Paginación personalizada
│   ├── middleware.py              # Middleware personalizado
│   └── urls.py                    # URLs de la aplicación
├── mysite/                        # Configuración del proyecto
│   ├── settings.py                # Configuración principal
│   ├── urls.py                    # URLs principales
│   └── wsgi.py                    # Configuración WSGI
├── static/                        # Archivos estáticos
├── tests/                         # Pruebas y scripts
├── MD/                            # Documentación adicional
├── requirements.txt               # Dependencias Python
├── Procfile                       # Configuración Railway
├── railway.json                   # Configuración Railway
├── .env.example                   # Ejemplo de variables de entorno
└── manage.py                      # Script de gestión Django
```

## 🧪 Pruebas

### Ejecutar Pruebas
```bash
python manage.py test
```

### Pruebas de API
```bash
pytest tests/
```

### Verificar Configuración
```bash
python manage.py check
```

## 🔧 Comandos Útiles

### Gestión de Datos
```bash
# Crear datos de prueba
python manage.py shell
>>> from tests.crear_datos_prueba import crear_datos_completos
>>> crear_datos_completos()

# Limpiar logs antiguos
python manage.py shell
>>> from blog.Models.AuditLogModel import AuditLog
>>> AuditLog.limpiar_logs_antiguos(dias=30)

# Generar estadísticas
python manage.py generar_estadisticas
```

### Desarrollo
```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python manage.py runserver 0.0.0.0:8000

# Ejecutar shell de Django
python manage.py shell

# Crear nueva migración
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

## 📈 Monitoreo y Logs

### Logs de Aplicación
Los logs se almacenan en:
- `logs/django.log` - Logs generales
- `logs/audit.log` - Logs de auditoría
- `logs/error.log` - Logs de errores

### Configuración de Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

### Proceso de Contribución
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código
- Seguir PEP 8 para Python
- Escribir tests para nuevas funcionalidades
- Documentar el código con docstrings
- Usar commits descriptivos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Miguel Bonilla** (@MiguelBonilla-sys)

- 🐙 GitHub: [@MiguelBonilla-sys](https://github.com/MiguelBonilla-sys)
- 📧 Email: [contacto disponible en el perfil de GitHub]

## 📞 Soporte

### Problemas y Sugerencias
- 🐛 **Issues**: [GitHub Issues](https://github.com/MiguelBonilla-sys/API_HACK3R/issues)
- 💡 **Sugerencias**: [GitHub Discussions](https://github.com/MiguelBonilla-sys/API_HACK3R/discussions)

### Recursos Útiles
- 📚 **Documentación Django**: https://docs.djangoproject.com/
- 🔧 **Django REST Framework**: https://www.django-rest-framework.org/
- 🚀 **Railway Docs**: https://docs.railway.app/

## 📊 Estado del Proyecto

- ✅ **API Funcional**: Todos los endpoints operativos
- ✅ **Despliegue**: Funcional en Railway
- ✅ **Autenticación**: Sistema completo implementado
- ✅ **Documentación**: Swagger/OpenAPI disponible
- ✅ **Auditoría**: Sistema de logs completo
- ✅ **Base de Datos**: PostgreSQL configurada
- ✅ **Almacenamiento**: Cloudinary integrado

---

⭐ **Si este proyecto te fue útil, no olvides darle una estrella en GitHub!**