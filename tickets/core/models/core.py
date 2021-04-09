from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class SupportParams(models.Model):
    identifier = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = _('Parámetros soporte')
        verbose_name_plural = _('Parámetros soporte')
        ordering = ['description']

    def __str__(self):
        return '{0} ({1}) {2}'.format(self.description, self.identifier, self.value)