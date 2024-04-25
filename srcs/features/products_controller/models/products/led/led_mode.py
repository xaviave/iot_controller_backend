from django.db import models
from polymorphic.models import PolymorphicModel


class LedMode(PolymorphicModel):
    name = models.CharField(max_length=200, unique=True)
    # add a field for temporary mode that will be cleaned by celery

    def __str__(self):
        return self.name

    def get_grpc_request(self) -> dict:
        raise NotImplementedError
