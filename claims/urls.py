from django.urls import path, include
from rest_framework.routers import DefaultRouter
from claims.views import ClaimViewSet

router = DefaultRouter()
router.register(r'', ClaimViewSet, basename='claim')

urlpatterns = [
    path('', include(router.urls)),
]
