from django.db import models
from django.core.exceptions import ValidationError
from items.models import Item
from users.models import Student


class Claim(models.Model):
    """Claim model for students claiming found items."""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimed_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='claims')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    evidence_file = models.FileField(upload_to='claim_evidence/', blank=True, null=True)
    claim_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'claim'
        ordering = ['-created_at']
        unique_together = ('item', 'claimed_by')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['claimed_by']),
        ]

    def clean(self) -> None:
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError({'status': 'Invalid claim status'})
        
        # Check for duplicate claims
        existing = Claim.objects.filter(
            item=self.item,
            claimed_by=self.claimed_by,
            status='Pending'
        ).exclude(id=self.id)
        if existing.exists():
            raise ValidationError('You already have a pending claim for this item')

    def __str__(self) -> str:
        return f"{self.claimed_by.first_name} - {self.item.name} ({self.status})"
