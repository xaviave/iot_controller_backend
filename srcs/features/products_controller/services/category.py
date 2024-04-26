from features.products_controller.models.category import Category
from features.products_controller.serializers.category import CategorySerializer
from features.products_controller.services.iot_mixin import IotMixin


class CategoryService(IotMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
