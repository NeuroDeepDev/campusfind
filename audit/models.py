from django.db import models
from items.models import Item
from claims.models import Claim
from users.models import Admin


class Audit(models.Model):
    """Audit log model for tracking changes."""
    
    action = models.CharField(max_length=100)
    affected_table = models.CharField(max_length=50)
    affected_id = models.IntegerField()
    changed_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    claim = models.ForeignKey(Claim, on_delete=models.SET_NULL, null=True, blank=True, related_name='audits')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='audits')
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['affected_table', 'affected_id']),
            models.Index(fields=['action']),
        ]

    def __str__(self) -> str:
        return f"{self.action} - {self.affected_table}:{self.affected_id}"
