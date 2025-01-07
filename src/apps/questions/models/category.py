import logging

from core.helpers.storage_helpers import handle_storage
from core.models import TimeStampedUUIDModel
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Category(TimeStampedUUIDModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Category name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Category description"),
    )
    icon = models.ImageField(
        null=True, blank=True, upload_to=handle_storage, verbose_name=_("Icon"), help_text=_("Category icon")
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
