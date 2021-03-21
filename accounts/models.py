from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    # Method to save user to the database
    def save_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Invalid Email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Call this method for password hashing
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    # Method called while creating a staff user
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    # Method called while calling creatsuperuser
    def create_superuser(self, email, password, **extra_fields):

        # Set is_superuser parameter to true
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')
        
        extra_fields['is_staff'] = True

        return self.save_user(email, password, **extra_fields) 
    

class User(AbstractBaseUser, PermissionsMixin):

    # Primary key of the model
    id = models.BigAutoField(
        primary_key = True,
    )

    first_name = models.CharField(
        max_length = 20,
        verbose_name = "First Name",
    )

    last_name = models.CharField(
        max_length = 20,
        verbose_name = "Last Name",
    )

    # Email field that serves as the username field
    email = models.CharField(
        max_length = 50, 
        unique = True, 
        validators = [validators.EmailValidator()],
        verbose_name = "Email"
    )

    # Other required fields for authentication
    # If the user is a staff, defaults to false
    is_staff = models.BooleanField(default=False)

    # If the user account is active or not. Defaults to True.
    # If the value is set to false, user will not be allowed to sign in.
    is_active = models.BooleanField(default=True)
    
    # Setting email instead of username
    USERNAME_FIELD = 'email'

    # Custom user manager
    objects = UserManager()

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name