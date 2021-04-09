import uuid

from django.utils.translation import ugettext as _
from django.db import models
from django.core.validators import FileExtensionValidator

class TicketType(models.Model):
    # Ticket type
    identifier = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

class Ticket(models.Model):
    # Ticket type
    identifier = models.CharField(max_length=255, blank=True, null=True, unique=True, default=uuid.uuid4)    
    ticket_type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='ticket/attachment/', null=True)            
    request_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='request_by')
    assign_to = models.ForeignKey('core.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='assign_to')    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class TicketComments(models.Model):
    # Ticket type
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='ticket/comment/', null=True)
    comment_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)