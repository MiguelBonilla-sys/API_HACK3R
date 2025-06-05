from django.contrib import admin
from blog.Models.CursosModel import Cursos
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.ProyectosModel import Proyectos
from blog.Models.NoticiasModel import Noticias
from blog.Models.AuditLogModel import AuditLog
from blog.Models.ConferenciasModel import Conferencias
from blog.Models.OfertasEmpleoModel import OfertasEmpleo

# Registrar modelos para que aparezcan en el panel de administración
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Configuración del admin para logs de auditoría."""
    list_display = ['timestamp', 'get_username', 'table_name', 'change_type', 'affected_record_id']
    list_filter = ['change_type', 'table_name', 'timestamp']
    search_fields = ['user__username', 'table_name', 'affected_record_id']
    readonly_fields = ['timestamp', 'user', 'table_name', 'change_type', 'affected_record_id', 'modified_data']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    def get_username(self, obj):
        """Mostrar username del usuario."""
        return obj.user.username if obj.user else "Usuario eliminado"
    get_username.short_description = 'Usuario'
    get_username.admin_order_field = 'user__username'
    
    def has_add_permission(self, request):
        """No permitir agregar logs manualmente."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """No permitir modificar logs."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Solo superusers pueden eliminar logs."""
        return request.user.is_superuser
admin.site.register(Conferencias)
admin.site.register(Cursos)
admin.site.register(Noticias)
admin.site.register(Integrantes)
admin.site.register(Proyectos)
admin.site.register(OfertasEmpleo)