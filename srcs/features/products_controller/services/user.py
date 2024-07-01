from django.contrib.auth.models import User
from features.products_controller.serializers.user import UserSerializer
from features.products_controller.services.iot_mixin import IotMixin


class UserService(IotMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
