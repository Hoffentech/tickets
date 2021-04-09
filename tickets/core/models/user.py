from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # Object manager for User

    def create_user(
        self, 
        email, 
        password=None, 
        is_active=True,
        is_staff=False,  
        **extra_fields
    ):
        
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )

        if password:
            user.set_password(password)
        
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, 
            password,
            is_staff=True,
            is_superuser=True, 
            **extra_fields
        )

class User(PermissionsMixin,AbstractBaseUser):    
    # User model
    name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')    
        ordering = ['email']  

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.email
