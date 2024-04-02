from asgiref.sync import sync_to_async
from django_socio_grpc import proto_serializers
from django_socio_grpc.proto_serializers import ListProtoSerializer
from django_socio_grpc.utils.constants import LIST_ATTR_MESSAGE_NAME
from features.products_controller.grpc.products_controller_pb2 import (
    ProjectListResponse,
    ProjectResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from features.products_controller.serializers.products.base_product import (
    BaseProductPolymorphicSerializer,
)
from rest_framework.serializers import LIST_SERIALIZER_KWARGS

LIST_PROTO_SERIALIZER_KWARGS = (*LIST_SERIALIZER_KWARGS, LIST_ATTR_MESSAGE_NAME, "message")


class ProjectListSerializer(ListProtoSerializer):
    def data_to_message(self, data):
        """
        List of protobuf messages <- List of dicts of python primitive datatypes.
        Add a custom serializer for Oneof
        """
        if data:
            for i, project in enumerate(data):
                new_products = [
                    {p["resourcetype"]: {k: p[k] for k in set(list(p.keys())) - set(["resourcetype"])}}
                    for p in project.get("products")
                ]
                data[i]["products"] = new_products
        return super().data_to_message(data)


class ProjectSerializer(proto_serializers.ModelProtoSerializer):
    products = BaseProductPolymorphicSerializer(many=True)

    # https://www.geeksforgeeks.org/prefetch_related-and-select_related-functions-in-django/
    class Meta:
        model = Project
        fields = "__all__"

        proto_class = ProjectResponse
        proto_class_list = ProjectListResponse

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        """
        Serialize the products to allow Oneof fields to be serialized into
        Polymorphic data types
        """
        if data.get("products") is not None:
            data["products"] = [{**p[next(iter(p))], "resourcetype": next(iter(p))} for p in data.get("products")]
        return super().to_internal_value(data)

    def create(self, validated_data):
        new_products = [
            BaseProduct.objects.get_or_create(name=p.get("name"))[0] for p in validated_data.pop("products", [])
        ]
        instance = Project.objects.create(**validated_data)
        instance.products.set(new_products)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.owner = validated_data.get("owner", instance.owner)
        instance.pub_date = validated_data.get("pub_date", instance.pub_date)
        instance.save()

        new_products = []
        for product in validated_data.pop("products", instance.products.all()):
            if isinstance(product, BaseProduct):
                name = product.name
            else:
                name = product.get("name")
            new_products.append(BaseProduct.objects.get_or_create(name=name)[0])
        instance.products.set(new_products)
        return instance

    @property
    async def raw_adata(self):
        """
        De-Serialize the products to allow Oneof fields to be transformed to a protobuf message
        while keeping the original data and dataset ids
        """
        adata = await sync_to_async(getattr)(self, "data")
        if adata.get("products") is not None:
            adata["products"] = [
                {p["resourcetype"]: {k: p[k] for k in set(list(p.keys())) - set(["resourcetype"])}}
                for p in adata.get("products")
            ]
        return adata

    @property
    async def amessage(self):
        """
        Surchage amessage to use raw_adata instead of adata
        """
        if not hasattr(self, "_message"):
            self._message = self.data_to_message(await self.raw_adata)
        return self._message

    @classmethod
    def many_init(cls, *args, **kwargs):
        """
        Surcharge the function to initialize the custom ProjectListSerializer
        instead of the ListProtoSerializer
        """
        allow_empty = kwargs.pop("allow_empty", None)
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {"child": child_serializer}
        if allow_empty is not None:
            list_kwargs["allow_empty"] = allow_empty
        list_kwargs.update({key: value for key, value in kwargs.items() if key in LIST_PROTO_SERIALIZER_KWARGS})
        meta = getattr(cls, "Meta", None)
        list_serializer_class = getattr(meta, "list_serializer_class", ProjectListSerializer)
        return list_serializer_class(*args, **list_kwargs)
