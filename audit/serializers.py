from rest_framework import serializers
from audit.models import Audit


class AuditSerializer(serializers.ModelSerializer):
    """Serializer for Audit model."""
    changed_by_name = serializers.CharField(source='changed_by.first_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Audit
        fields = ['id', 'action', 'affected_table', 'affected_id', 'changed_by', 'changed_by_name', 'claim', 'item', 'old_value', 'new_value', 'created_at']
        read_only_fields = ['id', 'created_at']
