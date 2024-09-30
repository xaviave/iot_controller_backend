from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django_socio_grpc import proto_serializers
from django_socio_grpc.proto_serializers import ListProtoSerializer
from django_socio_grpc.utils.constants import LIST_ATTR_MESSAGE_NAME
from rest_framework.serializers import LIST_SERIALIZER_KWARGS

from features.products_controller.grpc.products_controller_pb2 import ProjectListResponse, ProjectResponse
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from features.products_controller.serializers.products.base_product import BaseProductPolymorphicSerializer
from features.products_controller.serializers.user import UserSerializer

LIST_PROTO_SERIALIZER_KWARGS = (*LIST_SERIALIZER_KWARGS, LIST_ATTR_MESSAGE_NAME, "message")


def proto_dict_to_rest_dict(products: list[dict]) -> list[dict]:
    new_products = []
    for p in products:
        if p.get("resourcetype") is None:
            resourcetype = next(iter(p))
            p = {**p[resourcetype], "resourcetype": resourcetype}
        new_products.append(p)
    return new_products


def rest_dict_to_proto_dict(products: list[dict]) -> list[dict]:
    """
    rest polymorphic dict are {**data_dict, "resourcetype": resourcetype_class_name}
    proto dict are {"resourcetype_class_name": data_dict}.
    """
    new_products = []
    for p in products:
        if p.get("resourcetype") == "LedPanel":
            m = p["mode"]
            p["mode"] = {m["resourcetype"]: {k: m[k] for k in set(m.keys()) - {"resourcetype"}}}
        new_products.append({p["resourcetype"]: {k: p[k] for k in set(p.keys()) - {"resourcetype"}}})
    return new_products


class ProjectListSerializer(ListProtoSerializer):
    def data_to_message(self, data):
        """
        List of protobuf messages <- List of dicts of python primitive datatypes.
        Add a custom serializer for Oneof.
        """
        if data:
            for i, project in enumerate(data):
                data[i]["products"] = rest_dict_to_proto_dict(project["products"])
        return super().data_to_message(data)


class ProjectSerializer(proto_serializers.ModelProtoSerializer):
    owner = UserSerializer()
    products = BaseProductPolymorphicSerializer(many=True)

    # https://www.geeksforgeeks.org/prefetch_related-and-select_related-functions-in-django/
    class Meta:
        model = Project
        fields = "__all__"

        proto_class = ProjectResponse
        proto_class_list = ProjectListResponse

    def to_internal_value(self, data):
        """
        Serialize the products to allow Oneof fields to be serialized into
        Polymorphic data types.
        """
        if data.get("products") is not None:
            data["products"] = proto_dict_to_rest_dict(data["products"])
        return super().to_internal_value(data)

    def create(self, validated_data):
        try:
            owner = User.objects.get(username=validated_data.get("owner").get("username"))
        except User.DoesNotExist:
            serializer = UserSerializer(data=validated_data.get("owner"))
            serializer.is_valid(raise_exception=True)
            owner = serializer.save()
        new_products = []
        for product in validated_data.pop("products", []):
            try:
                p = BaseProduct.objects.get(name=product.get("name"))
            except BaseProduct.DoesNotExist:
                serializer = BaseProductPolymorphicSerializer(data=product)
                serializer.is_valid(raise_exception=True)
                p = serializer.save()
            new_products.append(p)

        validated_data["owner"] = owner
        instance = Project.objects.create(**validated_data)
        instance.products.set(new_products)
        return instance

    def update(self, instance, validated_data):
        # refacto to make sure the partial_update is smooth
        instance.name = validated_data.get("name", instance.name)
        instance.pub_date = validated_data.get("pub_date", instance.pub_date)

        if validated_data.get("owner") is not None:
            try:
                owner = User.objects.get(username=validated_data.get("owner").get("username"))
            except User.DoesNotExist:
                serializer = UserSerializer(data=validated_data.get("owner"))
                serializer.is_valid(raise_exception=True)
                owner = serializer.save()
            instance.owner = owner

        instance.save()

        if validated_data.get("products") is not None:
            new_products = []
            for product in validated_data.pop("products"):
                try:
                    p = BaseProduct.objects.get(name=product.get("name") if isinstance(product, dict) else product.name)
                    BaseProductPolymorphicSerializer().update(p, product)
                except BaseProduct.DoesNotExist:
                    serializer = BaseProductPolymorphicSerializer(data=product)
                    serializer.is_valid(raise_exception=True)
                    p = serializer.save()
                new_products.append(p)
            instance.products.set(new_products)
        return instance

    @property
    async def raw_adata(self):
        """
        De-Serialize the products to allow Oneof fields to be transformed to a protobuf message
        while keeping the original data and dataset ids.
        """
        adata = await sync_to_async(getattr)(self, "data")
        if adata.get("products") is not None:
            adata["products"] = rest_dict_to_proto_dict(adata["products"])
        return adata

    @property
    async def amessage(self):
        """Surchage amessage to use raw_adata instead of adata."""
        if not hasattr(self, "_message"):
            self._message = self.data_to_message(await self.raw_adata)
        return self._message

    @classmethod
    def many_init(cls, *args, **kwargs):
        """
        Surcharge the function to initialize the custom ProjectListSerializer
        instead of the ListProtoSerializer.
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
