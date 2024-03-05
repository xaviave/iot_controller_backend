import uuid

from django.db import models
from features.products_controller.models.category import Category
from polymorphic.models import PolymorphicModel


class BaseProduct(PolymorphicModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    @staticmethod
    def get_stub(channel):
        raise NotImplementedError
