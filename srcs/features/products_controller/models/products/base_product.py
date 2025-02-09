from typing import Never

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel

from features.products_controller.models.category import Category


class BaseProduct(PolymorphicModel):
    name = models.CharField(max_length=200, unique=True)
    ip_address = models.GenericIPAddressField(blank=False)
    ip_port = models.IntegerField(default=50051, validators=[MaxValueValidator(65536), MinValueValidator(0)])
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_stub() -> Never:
        raise NotImplementedError
