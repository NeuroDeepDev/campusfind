from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Category listing and retrieval."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
