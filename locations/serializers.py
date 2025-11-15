from rest_framework import serializers
from locations.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model."""
    
    class Meta:
        model = Location
        fields = ['id', 'building_name', 'building_code', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
