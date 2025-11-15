from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from claims.models import Claim
from claims.serializers import ClaimSerializer, ClaimDetailSerializer
from items.models import Item
from audit.models import Audit


class ClaimViewSet(viewsets.ModelViewSet):
    """ViewSet for Claim management."""
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item__name', 'claim_description']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return ClaimDetailSerializer
        return ClaimSerializer

    def perform_create(self, serializer):
        serializer.save(claimed_by=self.request.user)

    @action(detail=False, methods=['get'])
    def my_claims(self, request):
        """Get claims made by current user."""
        claims = self.queryset.filter(claimed_by=request.user)
        serializer = self.get_serializer(claims, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Admin action to approve a claim."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        claim = self.get_object()
        
        with transaction.atomic():
            claim.status = 'Approved'
            claim.save()
            
            item = claim.item
            item.status = 'Returned'
            item.save()
            
            Audit.objects.create(
                action='CLAIM_APPROVED',
                affected_table='claim',
                affected_id=claim.id,
                changed_by=request.user.admin if hasattr(request.user, 'admin') else None,
                claim=claim,
                item=item,
                new_value='Approved'
            )
        
        serializer = self.get_serializer(claim)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """Admin action to reject a claim."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        claim = self.get_object()
        
        with transaction.atomic():
            claim.status = 'Rejected'
            claim.save()
            
            Audit.objects.create(
                action='CLAIM_REJECTED',
                affected_table='claim',
                affected_id=claim.id,
                changed_by=request.user.admin if hasattr(request.user, 'admin') else None,
                claim=claim,
                new_value='Rejected'
            )
        
        serializer = self.get_serializer(claim)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        """Get all pending claims."""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        claims = self.queryset.filter(status='Pending')
        serializer = self.get_serializer(claims, many=True)
        return Response(serializer.data)
