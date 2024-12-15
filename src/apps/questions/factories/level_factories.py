from django.conf import settings
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyText
from questions.models import Level


class LevelFactory(DjangoModelFactory):
    class Meta:
        model = Level
        django_get_or_create = ("number",)

    name = FuzzyText(prefix="Level-")
    description = FuzzyText(prefix="Description-", length=50)
    number = FuzzyInteger(low=1, high=settings.MAX_LEVEL_ALLOWED)
