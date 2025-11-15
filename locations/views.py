from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from locations.models import Location
from locations.serializers import LocationSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Location listing and retrieval."""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]
    search_fields = ['building_name', 'building_code']
