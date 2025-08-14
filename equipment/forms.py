# equipment/forms.py
from django import forms
from .models import Equipment, EquipmentCategory
from .models import BorrowingRecord
from .models import RepairRequest

class EquipmentForm(forms.ModelForm):
    purchase_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False # Adjust as needed
    )
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'identifier', 'description', 
                  'quantity_total', 'quantity_available', 'status', 'purchase_date']
        # Optional: Add widgets for better UX
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_quantity_available(self):
        # Ensure available quantity is not more than total quantity
        available = self.cleaned_data.get('quantity_available')
        total = self.cleaned_data.get('quantity_total')
        if available is not None and total is not None and available > total:
            raise forms.ValidationError("Available quantity cannot exceed total quantity.")
        return available

class BorrowEquipmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta:
        model = BorrowingRecord
        fields = ['due_date'] # Only fields user needs to input
        # Consider adding 'notes' field if it's in your model

class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please describe the issue in detail...'}),
        }