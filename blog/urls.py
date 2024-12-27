from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
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


urlpatterns = [
    path('hl4/v1/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)