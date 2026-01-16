from django.db import models
from django.conf import settings


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    # optional OneToOne link to Django User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    dept = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_profile')
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    building = models.CharField(max_length=200)
    area = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.building} - {self.area or ''}"


class Item(models.Model):
    STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('RETURNED', 'Returned'),
    ]

    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    description = models.TextField(blank=True, null=True)
    found_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FOUND')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.item_id})"


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('FOUND', 'Found'),
        ('LOST', 'Lost'),
    ]

    report_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    report_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Report {self.report_id} - {self.report_type}"


class Claim(models.Model):
    CLAIM_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    claim_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimer = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='claims')
    claim_date = models.DateTimeField(auto_now_add=True)
    evidence = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CLAIM_STATUS, default='PENDING')

    def __str__(self):
        return f"Claim {self.claim_id} ({self.status})"


class Audit(models.Model):
    OP_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    audit_id = models.AutoField(primary_key=True)
    op_type = models.CharField(max_length=10, choices=OP_CHOICES)
    op_by = models.CharField(max_length=200, blank=True, null=True)
    op_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Audit {self.audit_id} - {self.op_type}"


class LostItem(models.Model):
    REPORTER_TYPE_CHOICES = [
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
        ('STAFF', 'Staff'),
        ('VISITOR', 'Visitor'),
    ]

    STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('RETURNED', 'Returned'),
    ]

    lost_item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200)
    item_type = models.CharField(max_length=200, blank=True, null=True)  # Add this
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lost_items')
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    contact_preference = models.CharField(max_length=20, choices=[('email', 'Email'), ('phone', 'Phone')])
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lost_reports')
    reporter_type = models.CharField(max_length=20, choices=REPORTER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='LOST')
    report_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lost Item: {self.item_name} ({self.lost_item_id})"
