from django import forms
from django.contrib.auth.models import User
from .models import SatisfactionPrediction

class PredictionForm(forms.ModelForm):
    class Meta:
        model = SatisfactionPrediction
        fields = ['compensation', 'career_progression', 'work_life_balance', 'manager_relationship']
        widgets = {
            field: forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-input-slider'})
            for field in ['compensation', 'career_progression', 'work_life_balance', 'manager_relationship']
        }
class HRRegistrationForm(forms.ModelForm):
    """
    Sleek authentication form to handle custom corporate email
    sign-ups and drive the custom verification modal flow.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'auth-input'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'auth-input'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'hr_manager_name', 'class': 'auth-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@company.com', 'class': 'auth-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class EngagementSlidersForm(forms.ModelForm):
    """
    Maps your 4 core organizational pillars directly to HTML5 range sliders
    to match your premium, Apple-inspired interface requirements.
    """

    class Meta:
        model = SatisfactionPrediction
        fields = ['compensation', 'career_progression', 'work_life_balance', 'manager_relationship']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Programmatically apply the premium range slider attributes to all 4 metrics
        for field_name in self.fields:
            self.fields[field_name].widget = forms.NumberInput(attrs={
                'type': 'range',
                'min': '1.0',
                'max': '10.0',
                'step': '0.1',
                'value': '5.0',
                'class': 'engageiq-slider'  # Custom class for your dark/orange CSS styling
            })