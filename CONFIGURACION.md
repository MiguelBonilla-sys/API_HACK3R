# Configuración del Proyecto Django

## Variables de Entorno Requeridas

Para que el proyecto funcione correctamente, necesitas configurar las siguientes variables de entorno:

### Configuración de Django
```bash
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=True  # False en producción
PRODUCTION=False  # True en producción
```

### Base de datos PostgreSQL
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### Configuración de Cloudinary (REQUERIDO para imágenes)
```bash
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### Redis para Celery (opcional)
```bash
REDIS_URL=redis://localhost:6379/0
```

### Para Railway
```bash
RAILWAY_ENVIRONMENT=production
```

### Para Vercel
```bash
VERCEL=1
VERCEL_ENV=production
VERCEL_URL=tu-app.vercel.app
```

### Para Render
```bash
RENDER=True
```

## Pasos para configurar:

1. **Crear archivo .env en la raíz del proyecto Django:**
   ```bash
   cd PruebaDJANGO
   touch .env
   ```

2. **Agregar las variables al archivo .env:**
   ```bash
   # Copiar las variables de arriba y reemplazar con tus valores reales
   SECRET_KEY=django-insecure-cambiar-esta-clave
   DEBUG=True
   DATABASE_URL=postgresql://tu_usuario:tu_password@tu_host:5432/tu_database
   CLOUDINARY_CLOUD_NAME=tu_cloud_name
   CLOUDINARY_API_KEY=tu_api_key
   CLOUDINARY_API_SECRET=tu_api_secret
   ```

3. **Obtener credenciales de Cloudinary:**
   - Registrarse en https://cloudinary.com/
   - Ir al Dashboard
   - Copiar Cloud Name, API Key y API Secret

4. **Configurar base de datos:**
   - Para Railway: la variable DATABASE_URL se configura automáticamente
   - Para desarrollo local: instalar PostgreSQL y crear una base de datos

## Problemas Comunes y Soluciones

### Error 500 al crear entidades con imágenes:
- **Causa:** Variables de Cloudinary no configuradas
- **Solución:** Configurar CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

### Error de conexión a base de datos:
- **Causa:** DATABASE_URL no configurada correctamente
- **Solución:** Verificar que la URL de PostgreSQL sea correcta

### Errores de CORS:
- **Causa:** Frontend en localhost:3000 no autorizado
- **Solución:** Ya configurado en settings.py, verificar CORS_ALLOWED_ORIGINS

### Debug no funciona:
- **Causa:** DEBUG=False por defecto en producción
- **Solución:** Configurar DEBUG=True para desarrollo local 