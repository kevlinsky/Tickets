from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    qr = forms.ImageField(label='QR code')

    class Meta:
        model = Ticket
        fields = (
            'number',
            'qr',
            'photo',
        )