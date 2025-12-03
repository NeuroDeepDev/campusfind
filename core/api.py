from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all().order_by('-item_id')
    serializer_class = ItemSerializer


router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='api-items')
