#!/bin/bash
# start.sh - Script de inicio para Railway

echo "🚀 Iniciando aplicación Django..."

# Crear directorio de logs solo si no estamos en producción
if [ -z "$RAILWAY_ENVIRONMENT" ] && [ -z "$VERCEL" ] && [ -z "$RENDER" ]; then
    echo "📁 Creando directorio de logs para desarrollo..."
    mkdir -p /app/logs
fi

# Verificar variables de entorno críticas
if [ -z "$SECRET_KEY" ]; then
    echo "❌ ERROR: SECRET_KEY no está configurado"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL no está configurado"
    exit 1
fi

echo "✅ Variables de entorno verificadas"

# Ejecutar migraciones si es necesario
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "🌐 Iniciando servidor Gunicorn..."
exec gunicorn mysite.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 30
