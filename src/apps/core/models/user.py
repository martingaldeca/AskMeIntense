import logging

from core.models import TimeStampedUUIDModel
from core.models.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


class User(AbstractUser, TimeStampedUUIDModel, PermissionsMixin):
    class AuthProviders(models.TextChoices):
        EMAIL_PROVIDER = ["email", _("Email")]
        GOOGLE_PROVIDER = ["google", _("Google")]

    username = None
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Email",
        help_text=_("User's email."),
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birthdate"),
        help_text=_("User's birthdate."),
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Is verified"),
        help_text=_("Field that shows if the user is verified or not."),
    )
    picture_url = models.URLField(
        default="https://pbs.twimg.com/media/ChDbQ2DWgAA7LGx.jpg",
        verbose_name=_("Picture URL"),
        help_text=_("Url of the picture profile. When auth login it will come from there."),
    )
    auth_provider = models.CharField(max_length=255, choices=AuthProviders, default=AuthProviders.EMAIL_PROVIDER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def verify(self):
        logger.info("User '%s' was verified", self)
        self.is_verified = True
        self.save()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @property
    def not_valid_login_method_message(self):
        match self.auth_provider:
            case self.AuthProviders.EMAIL_PROVIDER:
                return _("Please continue your login using email and password login")
            case self.AuthProviders.GOOGLE_PROVIDER:
                return _("Please continue your login using google login")
