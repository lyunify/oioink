from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have a username.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.is_email_verified = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',
                              max_length=128, unique=True)
    username = models.CharField(max_length=30, unique=True)
    signup_date = models.DateTimeField(
        verbose_name='signup date', auto_now_add=True)
    last_signin = models.DateTimeField(
        verbose_name='last signin', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


def profile_image_path(instance, file_name='profile_image.png'):
    return f'profile_images/{str(instance.pk)}/{file_name}'


def default_profile_image_path():
    return 'profile_images/0/default_profile_image.png'


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, unique=False)
    last_name = models.CharField(max_length=30, unique=False)
    phone = models.CharField(max_length=20, unique=False)
    address = models.CharField(max_length=100, unique=False)
    city = models.CharField(max_length=20, unique=False)
    country = models.CharField(max_length=20, unique=False)
    profile_image = models.ImageField(max_length=255, upload_to=profile_image_path,
                                      null=True, blank=True, default=default_profile_image_path)
    # Onboarding
    onboarding_completed = models.BooleanField(default=False, verbose_name='Onboarding Completed', 
                                               help_text='Whether the user has completed the onboarding tour')

    def __str__(self):
        return self.user.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + '/'):]
