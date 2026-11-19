from django import forms
from .models import DateSelection


class DateSelectionForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = DateSelection
        fields = [
            'name',
            'date_choice',
            'food_choice',
            'activity_choice',
            'message',
            'consent',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your beautiful name'
            }),
            'date_choice': forms.RadioSelect(),
            'food_choice': forms.RadioSelect(),
            'activity_choice': forms.RadioSelect(),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write something special...',
                'rows': 4
            }),
            'consent': forms.CheckboxInput(),
        }
