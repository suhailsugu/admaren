from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _

# Create your models here.



class UserManager(BaseUserManager):
    def create_user(self, username, password = None, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))

        user = self.model(username = username, **extra_fields)
        if password:
            user.set_password(password.strip())
            
        user.save()
        return user


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_admin', True)
     
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        
        return self.create_user(username, password, **extra_fields)




class Users(AbstractBaseUser, PermissionsMixin):
    class UserTypeChoice(models.TextChoices):
        Rider   = 'Rider'
        Driver  = 'Driver'
    
    email               = models.EmailField(_('Email'), max_length = 255, unique = True, blank = True, null = True)
    username            = models.CharField(_('User Name'), max_length = 300, blank = True, null = True)
    is_verified         = models.BooleanField(default = False)
    is_admin            = models.BooleanField(default = False)
    is_active           = models.BooleanField(default = True)
    is_staff            = models.BooleanField(default = False)
    is_superuser        = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True



