
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _

from backend.models import *

class TicketForm(forms.ModelForm):

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
        label=_("Título")
    )

    ticket_type = forms.ModelChoiceField(
        queryset= TicketType.objects.all(),
        empty_label= "Tipo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_("Tipo")
    )

    subject = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}),
        label=_("Asunto")
    )        

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label=_("Descripción")
    )        

    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'custom-file-input', 'placeholder': 'Imágen'}),
        label=_("Adjuntos")
    )
    
    class Meta:
        model = Ticket
        exclude = ['created_at', 'modified_at', 'assign_to', 'request_by', 'identifier']

    def clean(self):
        if self.instance.request_by:
            request_by = self.instance.invoice_number    
        else:
            request_by = self.request.user
        return self.cleaned_data