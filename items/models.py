from django.db import models
from django.core.exceptions import ValidationError
from categories.models import Category
from locations.models import Location
from users.models import Student


class Item(models.Model):
    """Item model for lost and found items."""
    
    STATUS_CHOICES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
        ('Returned', 'Returned'),
        ('Unclaimed', 'Unclaimed'),
    ]
    
    TYPE_CHOICES = [
        ('Found', 'Found'),
        ('Lost', 'Lost'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Found')
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True)
    reported_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reported_items')
    reported_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item'
        ordering = ['-reported_date']
        indexes = [
            models.Index(fields=['status', 'item_type']),
            models.Index(fields=['category']),
            models.Index(fields=['location']),
        ]

    def clean(self) -> None:
        if self.item_type not in dict(self.TYPE_CHOICES):
            raise ValidationError({'item_type': 'Invalid item type'})

    def __str__(self) -> str:
        return f"{self.name} ({self.item_type})"
