from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class Student(models.Model):
    """Student profile extending Django User model."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"


class Admin(models.Model):
    """Admin profile extending Django User model."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"
