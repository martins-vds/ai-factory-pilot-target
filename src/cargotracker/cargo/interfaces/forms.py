from django import forms


class TrackingForm(forms.Form):
    tracking_id = forms.CharField(
        error_messages={'required': 'tracking ID is required'},
        label='Tracking ID',
        strip=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'input input-bordered w-full',
                'placeholder': 'XYZ789',
            }
        ),
    )
