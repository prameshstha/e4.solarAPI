import binascii
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.template.loader import render_to_string
from django.utils import timezone

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMultiAlternatives

from DarwinSolar.settings import O365_Email
from DarwinSolar.utils import EmailThread, my_domain


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    link = "{}?token={}".format('password-reset-request', reset_password_token.key)
    print(sender, "sender", instance, "instance", reset_password_token, "reset_password_token",
          reset_password_token.user.email, *args)
    print(link)
    user = CustomUser.objects.get(email=reset_password_token.user.email)
    print(user.first_name, user.email)
    customer = user.first_name
    if user.first_name == '':
        customer = user.email
    print(customer)

    pw_reset_link = my_domain + link  # change in production level
    merge_data = {
        'customer': customer,
        'pw_reset_link': pw_reset_link  # change in production level
    }

    email_subject = "Password Reset for {title}".format(title="Darwin Solar Portal")
    email_html_body = render_to_string("reset_password_email.html", merge_data)
    from_email = "admin@darwinsolar.com.au"
    to_email = [reset_password_token.user.email]

    send_email = O365_Email.new_message(resource=from_email)
    send_email.to.add(to_email)
    send_email.subject = email_subject
    send_email.body = email_html_body
    send_email.send()
    print('should send email')
    # send_email = EmailMultiAlternatives(
    #     email_subject,
    #     email_html_body,
    #     from_email,
    #     to_email,
    #
    # )
    # send_email.attach_alternative(email_html_body, "text/html")
    # EmailThread(send_email).start()  # to send email faster


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The given Password must be set')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, default='lastname')
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(default=False)
    is_installer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    customer_crm_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name) + ' ' + str(self.email)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'


class InstallerUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The given Password must be set')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class InstallerUser(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        default=False,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    phone = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=120, null=True)
    city = models.CharField(max_length=120, null=True)
    postcode = models.IntegerField(null=True)
    state = models.CharField(max_length=120, null=True)
    country = models.CharField(max_length=120, null=True)
    # company = models.ManyToManyField(Company, on_delete=models.CASCADE, related_name='installer_of_company')
    is_installer = models.BooleanField(default=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name) + ' ' + str(self.email)

    objects = InstallerUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'InstallerUser'
        verbose_name_plural = 'InstallerUsers'


class InstallerToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField("Key", max_length=40, primary_key=True)

    user = models.ForeignKey(InstallerUser, related_name='installertokens', on_delete=models.CASCADE,
                                       verbose_name="InstallerUserToken"
                                       )

    class Meta:
        verbose_name = "InstallerToken"
        verbose_name_plural = "InstallerTokens"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(InstallerToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
