import logging

from core.models import TimeStampedUUIDModel
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Level(TimeStampedUUIDModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Level name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Level's description"),
    )
    number = models.IntegerField(
        verbose_name=_("Number"),
        help_text=_("Level's number. It will determine the grouping of the level"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(settings.MAX_LEVEL_ALLOWED),
        ],
        unique=True,
    )

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")
