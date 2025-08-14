from django.db import models

from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _                    # ValueError() raise garna use huncha

from django.contrib.auth import get_user_model




# Create your models here.

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, username=None, **extra_fields):                 # overriding inbuilt create_user() function
        
        User = self.model
        # User = get_user_model()

        if not email:
            raise ValueError(_('Please enter your valid email address'))
        
        # case-insensitive email uniqueness check
        email = email.lower()

        # Case-insensitive check after normalization
        if self.model.objects.filter(email__iexact=email).exists():
            raise ValueError("A user with that email already exists.")


        if username is None:                                                                # getting default username by splitting email
            username = email.split('@')[0]

        # if not username:
        #     raise ValueError(_('Please enter your username'))
        
        # if not first_name:
        #     raise ValueError(_('Please enter your firstname'))
        
        # if not last_name:
        #     raise ValueError(_('Please enter your lastname'))
        
        extra_fields.setdefault('is_active', True)
        # extra_fields.setdefault('is_active', False)

        extra_fields.setdefault('role', 'customer')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        email = self.normalize_email(email)

        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user




    def create_superuser(self, email, password, username=None, **extra_fields):            # overriding create_superuser() function 
    
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        # extra_fields.setdefault('is_active', False)
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
        
    username = models.CharField(_('Username'), max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(_('Email'), max_length=50, unique=True, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer') 
    date_joined = models.DateTimeField(_('Date'), auto_now_add=True)

    # REQUIRED_FIELDS = ['first_name', 'last_name', 'username']                      # Required fields for creating a user
    # REQUIRED_FIELDS = ['username']                                           # Required fields for creating a user, username is required
    REQUIRED_FIELDS = []                                       

    USERNAME_FIELD = 'email'                                                # email field le chai django ko username field jasto kaam garos vaneko

    objects = CustomUserManager()                                                                     # hamile banayeko CustomUserManager() vanni custom manager class lai call gareko .. objects lekhesi call huncha

    def __str__(self):                                                      # __str__() method is string representation of instance
        return f"User {self.username}"


    def save(self, *args, **kwargs):
        if User.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
            raise ValueError("A user with that email already exists.")

        super().save(*args, **kwargs)


    # # For unique email validation while creating new user from client side using API
    # # Database Level validation
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['email'],
    #             name='unique user email',
    #             condition=models.Q(email__isnull=False),
    #             violation_error_message="A user with that email already exists.",
    #         ),
    #     ]




