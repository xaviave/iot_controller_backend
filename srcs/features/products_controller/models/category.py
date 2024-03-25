import uuid
from django.db import models


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
