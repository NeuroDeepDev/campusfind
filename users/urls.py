from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import StudentViewSet, AdminViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'admins', AdminViewSet, basename='admin')

urlpatterns = [
    path('', include(router.urls)),
]
