from django.db import models


class Location(models.Model):
    """Location/Building model for item locations."""
    
    building_name = models.CharField(max_length=100, unique=True)
    building_code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'location'
        ordering = ['building_name']

    def __str__(self) -> str:
        return f"{self.building_name} ({self.building_code})"
