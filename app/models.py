from django.db import models

from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _                    # ValueError() raise garna use huncha



# Create your models here.

class CustomUserManager(BaseUserManager):
    
    def create_user(self, first_name, last_name, username, email, password, **extra_fields):                 # overriding inbuilt create_user() function
        
        if not email:
            raise ValueError(_('Please enter your valid email address'))

        if not first_name:
            raise ValueError(_('Please enter your firstname'))
        
        if not last_name:
            raise ValueError(_('Please enter your lastname'))
        
        if not username:
            raise ValueError(_('Please enter your username'))
        
        
        # extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_active', False)

        extra_fields.setdefault('role', 'customer')
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)

        return user




    def create_superuser(self, username, email, password, **extra_fields):            # overriding create_superuser() function 
        
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('role', 'admin') 


        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have 'is_superuser = True'"))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have 'is_staff = True'"))

        return self.create_user(username=username, email=email, password=password, **extra_fields)            # mathi override gareko create_user() method lai call garcha




class User(AbstractUser):                                                   # Extending from AbstractUser

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
        
    username = models.CharField(_('Username'), max_length=50, unique=True)

    email = models.EmailField(_('Email'), max_length=80, unique=True, blank=False)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer') 

    date_joined = models.DateTimeField(_('Date'), auto_now_add=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']                                           # Required fields for creating a user, username is required
    
    USERNAME_FIELD = 'email'                                                # email field le chai django ko username field jasto kaam garos vaneko

    objects = CustomUserManager()                                                                     # hamile banayeko CustomUserManager() vanni custom manager class lai call gareko .. objects lekhesi call huncha

    def __str__(self):                                                      # __str__() method is string representation of instance
        return f"User {self.username}"


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique user email',
                condition=models.Q(email__isnull=False),
                violation_error_message="A user with that email already exists.",
            ),
        ]




