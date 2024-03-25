import uuid
from django.contrib.auth.models import User
from django.db import models
from features.products_controller.models.products.base_product import BaseProduct


class Project(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    name = models.CharField(max_length=200, unique=True)
    products = models.ManyToManyField(BaseProduct)

    def __str__(self):
        return self.name
