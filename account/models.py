from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        if password != password2:
            raise ValueError('Passwords do not match')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, password2=None):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            password2=password2,
        )
        user.is_staff = True  # Set the user as staff
        user.is_superuser = True  # Set the user as superuser
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Indicates staff status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff  # Change this to appropriate permission logic

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)
    

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
