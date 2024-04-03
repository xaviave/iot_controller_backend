from django.db import models
from polymorphic.models import PolymorphicModel


class LedMode(PolymorphicModel):
    name = models.CharField(max_length=200, unique=True)
    # add a field for temporary mode that will be cleaned by celery

    @property
    def has_mode(self):
        return True

    @classmethod
    def mode_names(cls):
        return [m.__name__ for m in cls.__subclasses__()]

    def __str__(self):
        return self.name

    def get_mode_choices(self):
        return self.objects.all()

    def get_grpc_cmd(self) -> dict:
        raise NotImplementedError
