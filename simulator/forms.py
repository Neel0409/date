
from django import forms
from django.utils import timezone
from .models import DateSelection


class DateSelectionForm(forms.ModelForm):

    selected_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'id_selected_date',
            'class': 'date-input',
        }),
        error_messages={
            'required': 'Please choose when we should go on our date ❤️',
            'invalid': 'Please enter a valid date.',
        }
    )

    class Meta:
        model = DateSelection

        fields = [
            'name',
            'selected_date',
            'date_choice',
            'custom_date_choice',
            'food_choice',
            'custom_food_choice',
            'activity_choice',
            'custom_activity_choice',
            'message',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your beautiful name',
                'autocomplete': 'name',
            }),

            'date_choice': forms.RadioSelect(),

            'custom_date_choice': forms.TextInput(attrs={
                'placeholder': 'Tell me where you would like to go...',
                'id': 'id_custom_date_choice',
                'autocomplete': 'off',
            }),

            'food_choice': forms.RadioSelect(),

            'custom_food_choice': forms.TextInput(attrs={
                'placeholder': 'Tell me what you would like to eat...',
                'id': 'id_custom_food_choice',
                'autocomplete': 'off',
            }),

            'activity_choice': forms.RadioSelect(),

            'custom_activity_choice': forms.TextInput(attrs={
                'placeholder': 'What would you like us to do together?',
                'id': 'id_custom_activity_choice',
                'autocomplete': 'off',
            }),

            'message': forms.Textarea(attrs={
                'placeholder': 'Write something special...',
                'rows': 4,
            }),
        }

        error_messages = {
            'name': {
                'required': 'First, please tell me your name ❤️',
            },
            'date_choice': {
                'required': 'Please select where our date should be ❤️',
            },
            'food_choice': {
                'required': 'Please select what we should eat ❤️',
            },
            'activity_choice': {
                'required': 'Please select an activity for us ❤️',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        radio_fields = [
            'date_choice',
            'food_choice',
            'activity_choice',
        ]

        for field_name in radio_fields:
            field = self.fields[field_name]

            field.choices = [
                choice for choice in field.choices
                if choice[0] not in ('', None)
            ]

    def clean_selected_date(self):
        selected_date = self.cleaned_data.get('selected_date')

        if selected_date:
            today = timezone.localdate()

            if selected_date < today:
                raise forms.ValidationError(
                    'Please choose today or a future date for our date! ❤️'
                )

        return selected_date

    def clean(self):
        cleaned_data = super().clean()

        date_choice = cleaned_data.get('date_choice')
        custom_date_choice = cleaned_data.get('custom_date_choice')

        food_choice = cleaned_data.get('food_choice')
        custom_food_choice = cleaned_data.get('custom_food_choice')

        activity_choice = cleaned_data.get('activity_choice')
        custom_activity_choice = cleaned_data.get('custom_activity_choice')

        if date_choice == 'Other':
            if not custom_date_choice or not custom_date_choice.strip():
                self.add_error(
                    'custom_date_choice',
                    'Tell me where you would like to go... ❤️'
                )
        else:
            cleaned_data['custom_date_choice'] = ''

        if food_choice == 'Other':
            if not custom_food_choice or not custom_food_choice.strip():
                self.add_error(
                    'custom_food_choice',
                    'Tell me what you would like to eat... ❤️'
                )
        else:
            cleaned_data['custom_food_choice'] = ''

        if activity_choice == 'Other':
            if not custom_activity_choice or not custom_activity_choice.strip():
                self.add_error(
                    'custom_activity_choice',
                    'What would you like us to do together? ❤️'
                )
        else:
            cleaned_data['custom_activity_choice'] = ''

        return cleaned_data
