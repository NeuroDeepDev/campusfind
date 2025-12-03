from django import forms
from .models import Item, Report, Claim, Student


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'description', 'status', 'location']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['item', 'reporter', 'report_type', 'details']


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['item', 'claimer', 'evidence']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'dept', 'year']
