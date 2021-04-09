from django.db import models
from django.utils.translation import ugettext as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True     
                
class AuditableModel(models.Model):
    # Auditable model
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True, editable=False)
    created_by = models.ForeignKey('core.User', verbose_name=_('created by'), related_name="%(class)s_created_by", null=True,
                                   editable=False, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True, null=True, editable=False)
    updated_by = models.ForeignKey('core.User', verbose_name=_('updated by'), related_name="%(class)s_updated_by", null=True,
                                   editable=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True        
