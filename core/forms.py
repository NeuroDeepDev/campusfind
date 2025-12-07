from django import forms
from .models import Item, Report, Claim, Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
