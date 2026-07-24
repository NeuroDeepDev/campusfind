from django import forms
from .models import Item, Report, Claim, Student, LostItem, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DisabledPlaceholderSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None, **kwargs):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs, **kwargs)
        if value == '':
            option['attrs']['disabled'] = 'disabled'
        return option


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'description', 'status', 'location']


class ReportForm(forms.ModelForm):
    STANDARD_CATEGORY_CHOICES = [
        ('', 'Select any'),
        ('Electronics', 'Electronics'),
        ('Documents', 'Documents'),
        ('Jewelry & Valuables', 'Jewelry & Valuables'),
        ('Stationery & Books', 'Stationery & Books'),
        ('Personal Belongings', 'Personal Belongings'),
        ('Others', 'Others'),
    ]

    category = forms.ChoiceField(
        choices=STANDARD_CATEGORY_CHOICES,
        required=True,
        widget=DisabledPlaceholderSelect(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Report
        fields = [
            'item_name',
            'category',
            'report_type',
            'description',
            'brand',
            'model_number',
            'serial_number',
            'material',
            'engraving_details',
            'document_type',
            'color',
            'distinguishing_features',
            'location',
            'date_lost_found',
            'time_lost_found',
            'condition',
            'image1',
            'image2',
            'image3',
            'details',
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': 'e.g. Wallet, iPhone, Black backpack', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'report_type': forms.HiddenInput(attrs={'id': 'wizard-report-type'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the item in detail with identifying marks, colors, and condition.', 'rows': 4, 'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Brand or manufacturer (optional)', 'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'placeholder': 'Model number (electronics only)', 'class': 'form-control dynamic-field hidden'}),
            'serial_number': forms.TextInput(attrs={'placeholder': 'Serial number (electronics only)', 'class': 'form-control dynamic-field hidden'}),
            'material': forms.TextInput(attrs={'placeholder': 'Material (jewelry only)', 'class': 'form-control dynamic-field hidden'}),
            'engraving_details': forms.Textarea(attrs={'placeholder': 'Engraving or personalization details (jewelry only)', 'rows': 2, 'class': 'form-control dynamic-field hidden'}),
            'document_type': forms.TextInput(attrs={'placeholder': 'Type of document (documents only)', 'class': 'form-control dynamic-field hidden'}),
            'color': forms.TextInput(attrs={'placeholder': 'Color of the item', 'class': 'form-control'}),
            'distinguishing_features': forms.Textarea(attrs={'placeholder': 'Any scratches, stickers, or marks that stand out.', 'rows': 3, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where was the item lost or found?', 'class': 'form-control location-input'}),
            'date_lost_found': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_lost_found': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'placeholder': 'Condition for found items only', 'class': 'form-control found-only-field hidden'}),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control-file file-input', 'accept': 'image/png,image/jpeg'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control-file file-input', 'accept': 'image/png,image/jpeg'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control-file file-input', 'accept': 'image/png,image/jpeg'}),
            'details': forms.Textarea(attrs={'placeholder': 'Any additional context that may help recover the item.', 'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'item_name': 'Item Name',
            'category': 'Category',
            'description': 'Detailed Description',
            'location': 'Lost/Found Location',
            'date_lost_found': 'Date Lost/Found',
            'time_lost_found': 'Time Lost/Found (Optional)',
            'details': 'Additional Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = self.STANDARD_CATEGORY_CHOICES
        self.fields['item_name'].required = True
        self.fields['category'].required = True
        self.fields['description'].required = True
        self.fields['location'].required = True
        self.fields['date_lost_found'].required = True
        self.fields['item_name'].widget.attrs['required'] = 'required'
        self.fields['category'].widget.attrs['required'] = 'required'
        self.fields['description'].widget.attrs['required'] = 'required'
        self.fields['location'].widget.attrs['required'] = 'required'
        self.fields['date_lost_found'].widget.attrs['required'] = 'required'

    def clean(self):
        cleaned_data = super().clean()
        item_name = cleaned_data.get('item_name')
        category = cleaned_data.get('category')
        location = cleaned_data.get('location')
        date_lost_found = cleaned_data.get('date_lost_found')

        if not item_name:
            raise forms.ValidationError('Please enter the item name.')

        if not category:
            raise forms.ValidationError('Please select a category for the report.')

        if not location:
            raise forms.ValidationError('Please enter the lost/found location.')

        if not date_lost_found:
            raise forms.ValidationError('Please enter the date lost or found.')

        return cleaned_data

    def save(self, commit=True):
        report = super().save(commit=False)
        category_name = self.cleaned_data.get('category')
        if category_name:
            category_obj, _ = Category.objects.get_or_create(category_name=category_name)
            report.category = category_obj
        if commit:
            report.save()
        return report


class ClaimForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), required=True, widget=forms.HiddenInput())
    claimant_name = forms.CharField(max_length=200, required=True, label='Full Name')
    claimant_email = forms.EmailField(required=True, label='Email Address')
    claimant_phone = forms.CharField(max_length=50, required=True, label='Phone Number')
    identity_proof = forms.FileField(required=True, label='Identity Proof *')
    ownership_proof = forms.FileField(required=True, label='Ownership Proof *')
    ownership_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe the item, its brand, color, distinguishing marks, approximate date lost, contents, and any unique identifiers.'}), label='Ownership Description *')
    additional_evidence = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add any extra context or supporting notes (optional).'}), label='Additional Supporting Evidence')
    declaration_confirmed = forms.BooleanField(required=True, label='I confirm that the information provided is accurate and truthful.')

    def __init__(self, *args, **kwargs):
        self.item_instance = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)
        if self.item_instance:
            self.fields['item'].initial = self.item_instance.item_id
            self.fields['item'].widget = forms.HiddenInput()
            self.fields['item'].queryset = Item.objects.filter(pk=self.item_instance.pk)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('item') and self.item_instance:
            cleaned_data['item'] = self.item_instance
        return cleaned_data

    def save(self, commit=True):
        item = self.cleaned_data['item']
        claimant_name = self.cleaned_data['claimant_name']
        claimant_email = self.cleaned_data['claimant_email']
        claimant_phone = self.cleaned_data['claimant_phone']
        ownership_description = self.cleaned_data['ownership_description']
        additional_evidence = self.cleaned_data['additional_evidence']
        identity_proof = self.cleaned_data['identity_proof']
        ownership_proof = self.cleaned_data['ownership_proof']

        student = None
        if self.item_instance and self.item_instance.status == 'FOUND':
            try:
                student = Student.objects.get(email__iexact=claimant_email)
            except Student.DoesNotExist:
                student = None

        claim = Claim.objects.create(
            item=item,
            claimer=student,
            evidence=f"{ownership_description}\n\nAdditional evidence: {additional_evidence or 'None'}",
            status='PENDING',
        )

        if commit:
            claim.save()
        return claim


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
