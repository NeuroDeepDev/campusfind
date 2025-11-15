from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from items.models import Item
from items.serializers import ItemSerializer, ItemDetailSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for Item management."""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['reported_date', 'created_at']
    ordering = ['-reported_date']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return ItemDetailSerializer
        return ItemSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def found_items(self, request):
        """Get all found items that are unclaimed."""
        items = self.queryset.filter(item_type='Found', status__in=['Found', 'Unclaimed'])
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def lost_items(self, request):
        """Get all lost items."""
        items = self.queryset.filter(item_type='Lost')
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_items(self, request):
        """Get items reported by current user."""
        items = self.queryset.filter(reported_by=request.user)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def detail(self, request, pk=None):
        """Get detailed item information."""
        item = self.get_object()
        serializer = ItemDetailSerializer(item)
        return Response(serializer.data)
