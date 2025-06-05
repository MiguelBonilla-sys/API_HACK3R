from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from blog.Views.AuditLogView import AuditLogViewSet
from blog.Views.ConferenciasView import ConferenciasViewSet
from blog.Views.CursosView import CursosViewSet
from blog.Views.IntegrantesView import IntegrantesViewSet
from blog.Views.NoticiasView import NoticiasViewSet
from blog.Views.OfertasEmpleoView import OfertasEmpleoViewSet
from blog.Views.ProyectosView import ProyectosViewSet
from blog.Views.AuthView import user_profile, update_profile, check_auth_status
from blog.Views.AuditVerificationView import audit_verification_status, audit_logs_simple, test_audit_trigger
from blog.Views.PermissionsView import (
    get_my_permissions,
    check_permission,
    get_available_permissions,
    get_group_perms
)

router = routers.DefaultRouter()
router.register(r'auditlog', AuditLogViewSet)
router.register(r'conferencias', ConferenciasViewSet)
router.register(r'cursos', CursosViewSet)
router.register(r'integrantes', IntegrantesViewSet)
router.register(r'noticias', NoticiasViewSet)
router.register(r'ofertasempleo', OfertasEmpleoViewSet)
router.register(r'proyectos', ProyectosViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API title",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# URLs de la API
urlpatterns = [
    path('', include(router.urls)),
    
    # URLs de autenticación y perfil
    path('profile/', user_profile, name='user-profile'),
    path('profile/update/', update_profile, name='update-profile'),
    path('auth/status/', check_auth_status, name='auth-status'),
    
    # URLs de auditoría
    path('audit/verify/', audit_verification_status, name='audit-verify'),
    path('audit/logs/simple/', audit_logs_simple, name='audit-logs-simple'),
    path('audit/test/', test_audit_trigger, name='audit-test'),
    
    # URLs de permisos
    path('permissions/', get_my_permissions, name='my-permissions'),
    path('permissions/check/', check_permission, name='check-permission'),
    path('permissions/available/', get_available_permissions, name='available-permissions'),
    path('permissions/group/<str:group_name>/', get_group_perms, name='group-permissions'),
    
    # URLs de documentación
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]