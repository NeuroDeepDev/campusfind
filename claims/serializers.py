from rest_framework import serializers
from claims.models import Claim


class ClaimSerializer(serializers.ModelSerializer):
    """Serializer for Claim model."""
    item_name = serializers.CharField(source='item.name', read_only=True)
    claimed_by_name = serializers.CharField(source='claimed_by.first_name', read_only=True)
    
    class Meta:
        model = Claim
        fields = ['id', 'item', 'item_name', 'claimed_by', 'claimed_by_name', 'status', 'evidence_file', 'claim_description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'claimed_by']


class ClaimDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Claim model."""
    item = serializers.SerializerMethodField()
    
    class Meta:
        model = Claim
        fields = ['id', 'item', 'claimed_by', 'status', 'evidence_file', 'claim_description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'claimed_by']

    def get_item(self, obj):
        from items.serializers import ItemSerializer
        return ItemSerializer(obj.item).data

    def create(self, validated_data):
        validated_data['claimed_by'] = self.context['request'].user
        return super().create(validated_data)
