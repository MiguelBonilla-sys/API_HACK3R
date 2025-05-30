#!/bin/bash
# start.sh - Script de inicio para Railway

set -e  # Salir si hay algún error

echo "🚀 Iniciando aplicación Django..."

# Verificar variables de entorno críticas
if [ -z "$SECRET_KEY" ]; then
    echo "❌ ERROR: SECRET_KEY no está configurado"
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
exec gunicorn mysite.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --max-requests 1000
