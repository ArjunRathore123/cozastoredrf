from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
class UserManager(BaseUserManager):
    def create_user(self,email,password,**efields):
        if not email:
            raise ValueError('Email must be set')
        email=self.normalize_email(email)
        user=self.model(email=email,**efields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,email,password,**efields):
        efields.setdefault('is_staff',True)
        efields.setdefault('is_superuser',True)
        efields.setdefault('is_active',True)

        if efields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if efields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email=email,password=password,**efields)

        