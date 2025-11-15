from rest_framework import serializers
from items.models import Item
from categories.serializers import CategorySerializer
from locations.serializers import LocationSerializer
from users.serializers import StudentSerializer


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    location_name = serializers.CharField(source='location.building_name', read_only=True)
    reported_by_name = serializers.CharField(source='reported_by.first_name', read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category', 'category_name', 'location', 'location_name', 'status', 'item_type', 'evidence_file', 'reported_by', 'reported_by_name', 'reported_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reported_date', 'created_at', 'updated_at', 'reported_by']


class ItemDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Item model."""
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    reported_by = StudentSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    location_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category', 'category_id', 'location', 'location_id', 'status', 'item_type', 'evidence_file', 'reported_by', 'reported_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reported_date', 'created_at', 'updated_at', 'reported_by']

    def create(self, validated_data):
        validated_data['reported_by'] = self.context['request'].user
        return super().create(validated_data)
