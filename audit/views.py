from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from audit.models import Audit
from audit.serializers import AuditSerializer


class AuditViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Audit log viewing."""
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'affected_table']
    ordering_fields = ['created_at', 'action']
    ordering = ['-created_at']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Audit.objects.none()
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def by_action(self, request):
        """Get audit logs filtered by action."""
        action_name = request.query_params.get('action')
        if action_name:
            logs = self.queryset.filter(action=action_name)
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({'error': 'Action parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def claim_history(self, request):
        """Get audit history for a specific claim."""
        claim_id = request.query_params.get('claim_id')
        if claim_id:
            logs = self.queryset.filter(claim_id=claim_id)
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({'error': 'claim_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
