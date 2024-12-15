from core.helpers import UUIDModelSerializerMixin
from questions.models import Level


class LevelSerializer(UUIDModelSerializerMixin):
    class Meta:
        model = Level
        fields = ["uuid", "name", "description", "number"]
