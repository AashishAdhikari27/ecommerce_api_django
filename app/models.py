from django.db import models

from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _                    # ValueError() raise garna use huncha



# Create your models here.

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):                 # overriding inbuilt create_user() function
        
        if not email:
            raise ValueError(_('Please enter an email address'))

        email = self.normalize_email(email)                                 # normalize_email() le email lai lowercase ma laijancha

        new_user = self.model(email=email, **extra_fields)

        new_user.set_password(password)                                     # set_password() method hashes the password

        new_user.save()                                                     # new user lai database table ma save garcha

        return new_user



    def create_superuser(self, email, password, **extra_fields):            # overriding create_superuser() function 
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have 'is_superuser = True'"))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have 'is_staff = True'"))

        return self.create_user(email, password, **extra_fields)            # mathi override gareko create_user() method lai call garcha




class User(AbstractUser):                                                   # Extending from AbstractUser
    username = models.CharField(_('Username'), max_length=50, unique=True)
    email = models.EmailField(_('Email'), max_length=80, unique=True, blank=False)
    date_joined = models.DateTimeField(_('Date'), auto_now_add=True)

    REQUIRED_FIELDS = []
    
    USERNAME_FIELD = 'email'                                                # email field le chai django ko username field jasto kaam garos vaneko

    objects = CustomUserManager()                                                                     # hamile banayeko CustomUserManager() vanni custom manager class lai call gareko .. objects lekhesi call huncha

    def __str__(self):                                                      # __str__() method is string representation of instance
        return f"User {self.username}"






