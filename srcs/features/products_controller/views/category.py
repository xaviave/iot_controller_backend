from django_socio_grpc import generics
from features.products_controller.models.category import Category
from features.products_controller.serializers.category import CategorySerializer


class CategoryService(generics.AsyncModelService):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
