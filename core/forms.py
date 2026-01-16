from django import forms
from .models import Item, Report, Claim, Student, LostItem
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


class LostItemForm(forms.ModelForm):
    item_type = forms.ChoiceField(choices=[], required=False)  # Dynamic choices

    class Meta:
        model = LostItem
        fields = ['item_name', 'item_type', 'description', 'category', 'location', 'date_time', 'image', 'contact_preference']
        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Brief description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location of loss'}),
            'date_time': forms.DateTimeInput(attrs={'placeholder': 'Date & Time of loss'}),
            'image': forms.ClearableFileInput(attrs={'required': False}),
            'contact_preference': forms.Select(choices=[('email', 'Email'), ('phone', 'Phone')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial empty choices for item_type
        self.fields['item_type'].choices = []
