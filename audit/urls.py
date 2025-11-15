from django.urls import path, include
from rest_framework.routers import DefaultRouter
from audit.views import AuditViewSet

router = DefaultRouter()
router.register(r'', AuditViewSet, basename='audit')

urlpatterns = [
    path('', include(router.urls)),
]
