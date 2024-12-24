from django.core.files.base import ContentFile
from factory import LazyAttribute
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyText
from questions.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = FuzzyText(prefix="Category-")
    description = FuzzyText(prefix="Description-", length=50)
    icon = LazyAttribute(lambda _: ContentFile(ImageField()._make_data({"width": 1024, "height": 768}), "icon.png"))
