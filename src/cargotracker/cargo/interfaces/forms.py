from django import forms


class TrackingForm(forms.Form):
    tracking_id = forms.CharField(
        error_messages={'required': 'tracking ID is required'},
        label='Tracking ID',
        strip=True,
        widget=forms.TextInput(
            attrs={
                'class': (
                    'input input-bordered block w-full rounded-md border border-slate-300 px-3 py-2'
                ),
                'placeholder': 'XYZ789',
            }
        ),
    )
