from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, User
from django.contrib.sessions.models import Session
from django.db import models
from django.urls import reverse


# Create your models here.
class UserModuleManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        email, password, False, **data
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # user.is_active=False
        user.save()
        created = True
        return user, created

    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        # raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user_manager', kwargs={'pk': self.pk})


class User(AbstractBaseUser, PermissionsMixin):
    """creates a usermodel that supports email address instead of username"""

    class Meta:
        db_table = 'user_manager'  # define your custom name

    country_code_choices = [("KE", "Kenya"), ("UG", "Uganda"), ("TZ", "Tanzania"), ("SS", "South Sudan"),
                            ("RW", "Rwanda"), ("ET", "Ethiopia"), ("DRC",
                                                                   "Democratic Repuplic of Congo"),
                            ("BCDC", "BCDC"), ]

    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255, default=False)
    last_name = models.CharField(max_length=255, default=False)
    gender = models.CharField(max_length=255, default=False)
    country_code = models.CharField(
        max_length=255, choices=country_code_choices, default=False)

    # username = models.CharField(max_length=255, default=True, unique=True)
    phone = models.CharField(max_length=255, default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    dob = models.DateTimeField(auto_created=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # password = models.CharField(max_length=255, default=False)
    # hash = models.CharField(max_length=255, default=False)
    # roles[]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserModuleManager()


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
