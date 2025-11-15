from django.db import models
from django.core.exceptions import ValidationError
from items.models import Item
from users.models import Student


class Report(models.Model):
    """Report model for lost/found item reports."""
    
    TYPE_CHOICES = [
        ('Found', 'Found'),
        ('Lost', 'Lost'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField()
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'report'
        ordering = ['-created_at']

    def clean(self) -> None:
        if self.report_type not in dict(self.TYPE_CHOICES):
            raise ValidationError({'report_type': 'Invalid report type'})

    def __str__(self) -> str:
        return f"{self.report_type} - {self.item.name}"
