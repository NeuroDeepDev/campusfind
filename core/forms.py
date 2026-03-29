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
    username = forms.CharField(required=True, max_length=150, label='Username')
    name = forms.CharField(required=True, max_length=200, label='Full Name')
    email = forms.EmailField(required=False, label='Gmail ID', help_text='Optional; must be a Gmail address if provided.')
    phone = forms.CharField(required=False, max_length=20, label='Phone Number', help_text='Optional; use international format if possible.')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').strip()
        phone = cleaned_data.get('phone', '').strip()

        if not email and not phone:
            raise forms.ValidationError('Please provide either a Gmail ID or a phone number.')

        if email and not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError('Please provide a valid Gmail address (example@gmail.com).')

        cleaned_data['email'] = email
        cleaned_data['phone'] = phone
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email', '').strip()
        user.email = email
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
