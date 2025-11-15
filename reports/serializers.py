from rest_framework import serializers
from reports.models import Report
from items.serializers import ItemSerializer


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model."""
    item_name = serializers.CharField(source='item.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.first_name', read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'item', 'item_name', 'report_type', 'description', 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class ReportDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Report model."""
    item = ItemSerializer(read_only=True)
    item_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'item', 'item_id', 'report_type', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
