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

urlpatterns = [
    path('hl4/v1/', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]