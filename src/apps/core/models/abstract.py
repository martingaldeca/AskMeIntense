import logging
import uuid

from django.db import models
from model_utils import models as model_utils_models

logger = logging.getLogger(__name__)


class UUIDModel(models.Model):
    """
    This model allows you to have an indexed uuid field that should be unique
    """

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        """
        The default str representation for a model that inheritance from this mmodel will
        return the uuid and the id, so you can identify it faster and better in the logs
        if needed
        :return:
        """
        if hasattr(self, "id"):
            if hasattr(self, "name"):
                return f"{self.id}-{self.name}"
            return f"{self.id}-{self.uuid.hex}"
        return self.uuid


class TimeStampedUUIDModel(UUIDModel, model_utils_models.TimeStampedModel):
    """
    This model is the combination of the UUID model and the timestamped model provided by
    mode utils. You should use this abstract model in all your models, as it adds extra
    functionalities that are very useful.
    """

    class Meta:
        abstract = True
