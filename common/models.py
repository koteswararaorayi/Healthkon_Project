from django.db import models
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import UserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email,  password, alias=None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.save()
        return user

class MyNewUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    healthkon_id = models.CharField(max_length=50)
    account_id = models.CharField(max_length=32)
    email = models.EmailField(unique=True, max_length=64)
    mobile = models.CharField(max_length=15)
    project_id = models.CharField(max_length=32)
    location_id = models.CharField(max_length=32)
    roleid = models.PositiveSmallIntegerField()
    speciality_id = models.PositiveSmallIntegerField()
    token = models.CharField(max_length=64)
    ehr_token = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    api_token = models.CharField(max_length=80)
    remember_token = models.CharField(max_length=100)
    confirmation_code = models.CharField(max_length=255)
    uid = models.CharField(max_length=32)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email &amp; Password are required by default.

    class Meta:
        db_table = "newusers"

    def __str__(self):
        return str(self.email)

class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    healthkon_id = models.CharField(max_length=50, null=True)
    account_id = models.CharField(max_length=32, null=True)
    email = models.EmailField(unique=True, max_length=64)
    mobile = models.CharField(max_length=15)
    project_id = models.CharField(max_length=32, null=True)
    location_id = models.CharField(max_length=32, null=True)
    roleid = models.PositiveSmallIntegerField()
    speciality_id = models.PositiveSmallIntegerField(null=True)
    token = models.CharField(max_length=64, null=True)
    ehr_token = models.CharField(max_length=128, null=True)
    password = models.CharField(max_length=128)
    api_token = models.CharField(max_length=80, null=True)
    remember_token = models.CharField(max_length=100, null=True)
    confirmation_code = models.CharField(max_length=255, null=True)
    uid = models.CharField(max_length=32, null=True)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email &amp; Password are required by default.

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.email)

# Create your models here.
