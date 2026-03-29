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
    contact = forms.CharField(required=True, max_length=254, label='Gmail ID or Phone Number',
        help_text='Enter either your Gmail (example@gmail.com) or phone number.')

    class Meta:
        model = User
        fields = ('username', 'name', 'contact', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        contact = cleaned_data.get('contact', '').strip()

        if not contact:
            raise forms.ValidationError('Please provide your Gmail ID or phone number.')

        if '@' in contact:
            if not contact.lower().endswith('@gmail.com'):
                raise forms.ValidationError('Please provide a valid Gmail address (must end with @gmail.com).')
            cleaned_data['email'] = contact.lower()
            cleaned_data['phone'] = ''
        else:
            phone = ''.join([c for c in contact if c.isdigit() or c == '+'])
            if not phone or len(phone) < 7:
                raise forms.ValidationError('Please provide a valid phone number with at least 7 digits.')
            cleaned_data['phone'] = phone
            cleaned_data['email'] = ''

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        contact_email = self.cleaned_data.get('email', '')
        user.email = contact_email
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
