
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _

from core.models import User
from backend.models import *

class TicketForm(forms.ModelForm):

    ticket_type = forms.ModelChoiceField(
        queryset= TicketType.objects.all(),
        empty_label= "Tipo",
        widget=forms.Select(attrs={'class': 'form-control mb-4'}),
        label=_("Tipo")
    )

    subject = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Asunto'}),
        label=_("Asunto")
    )        

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'rows': 3}),
        label=_("Descripción")
    )        

    attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Adjunto'}),
        label=_("Adjunto")
    )

    request_by = forms.CharField(required=False,widget=forms.HiddenInput())
    
    class Meta:
        model = Ticket
        exclude = ['created_at', 'modified_at', 'assign_to', 'identifier']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):        
        if self.instance.request_by is not None:
            self.cleaned_data['request_by'] = self.instance.request_by    
        else:
            self.cleaned_data['request_by'] = self.request.user
        
        return self.cleaned_data


class UserForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
        label=_("Nombre")
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
        label=_("Email")
    )

    class Meta:
        model = User
        fields = ("name", "email", "is_active")     

