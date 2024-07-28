from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from .manager import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, validators=[EmailValidator()])
    username = models.CharField(_('username'), max_length=150, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ("date_joined",)
        verbose_name = _("user")
        verbose_name_plural = _("users")
        app_label = "accounts"

    def clean(self):
        super().clean()
        if CustomUser.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': _('Email must be unique')})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.username

    def __str__(self):
        return self.email


class SubscriberProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber_profile'
    )

    def __str__(self):
        return f"{self.user.get_full_name()}'s Subscriber Profile"


class AuthorProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author_profile'
    )

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}'s Author Profile"



