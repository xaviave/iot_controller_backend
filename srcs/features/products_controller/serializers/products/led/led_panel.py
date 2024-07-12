from asgiref.sync import sync_to_async
from django_socio_grpc import proto_serializers
from django_socio_grpc.proto_serializers import ListProtoSerializer
from django_socio_grpc.utils.constants import LIST_ATTR_MESSAGE_NAME
from features.products_controller.grpc.products_controller_pb2 import (
    LedPanelListResponse,
    LedPanelResponse,
)
from features.products_controller.models.category import Category
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.category import CategorySerializer
from features.products_controller.serializers.products.led.led_mode import (
    LedModePolymorphicSerializer,
)
from rest_framework import serializers
from rest_framework.serializers import LIST_SERIALIZER_KWARGS

LIST_PROTO_SERIALIZER_KWARGS = (*LIST_SERIALIZER_KWARGS, LIST_ATTR_MESSAGE_NAME, "message")


class LedPanelListSerializer(ListProtoSerializer):
    def data_to_message(self, data):
        """
        List of protobuf messages <- List of dicts of python primitive datatypes.
        Add a custom serializer for Oneof
        """
        if data:
            for i, mode in enumerate(data):
                m = mode.get("mode")
                data[i]["mode"] = {m["resourcetype"]: {k: m[k] for k in set(list(m.keys())) - set(["resourcetype"])}}
        return super().data_to_message(data)


class LedPanelSerializer(proto_serializers.ModelProtoSerializer):
    mode = LedModePolymorphicSerializer(many=False)
    name = serializers.CharField(validators=[])
    categories = CategorySerializer(many=True)

    class Meta:
        model = LedPanel
        fields = "__all__"

        proto_class = LedPanelResponse
        proto_class_list = LedPanelListResponse

    def to_internal_value(self, data):
        """
        Serialize the products to allow Oneof fields to be serialized into
        Polymorphic data types
        """
        if data.get("mode") is not None:
            m = data.get("mode")
            if m.get("resourcetype") is None:
                resourcetype = next(iter(m))
                data["mode"] = {**m[resourcetype], "resourcetype": resourcetype}
        return super().to_internal_value(data)

    def create(self, validated_data):
        new_categories = []
        for c in validated_data.pop("categories", []):
            try:
                c = Category.objects.get(name=c.get("name"))
            except Category.DoesNotExist:
                serializer = CategorySerializer(data=c)
                serializer.is_valid(raise_exception=True)
                c = serializer.save()
            new_categories.append(c)

        led_mode_data = validated_data.pop("mode")
        try:
            led_mode = LedMode.objects.get(name=led_mode_data.get("name"))
        except LedMode.DoesNotExist:
            serializer = LedModePolymorphicSerializer(data=led_mode_data)
            serializer.is_valid(raise_exception=True)
            led_mode = serializer.save()

        instance = LedPanel.objects.create(mode=led_mode, **validated_data)
        instance.categories.set(new_categories)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.brightness = validated_data.get("brightness", instance.brightness)

        if "mode" in validated_data.keys():
            try:
                instance.mode = LedMode.objects.get(name=validated_data.get("mode").get("name"))
                LedModePolymorphicSerializer().update(instance.mode, validated_data.get("mode"))
            except LedMode.DoesNotExist:
                serializer = LedModePolymorphicSerializer(data=validated_data.get("mode"))
                serializer.is_valid(raise_exception=True)
                instance.mode = serializer.save()
        instance.save()

        if "mode" not in validated_data.keys():
            return instance
        
        new_categories = []
        categories = validated_data.pop("categories", instance.categories.all())
        for category in categories:
            try:
                c = Category.objects.get(name=category.get("name") if isinstance(category, dict) else category.name)
                CategorySerializer().update(c, category)
            except Category.DoesNotExist:
                serializer = CategorySerializer(data=category)
                serializer.is_valid(raise_exception=True)
                c = serializer.save()
            new_categories.append(c)
        instance.categories.set(new_categories)
        return instance

    @property
    async def raw_adata(self):
        """
        De-Serialize the products to allow Oneof fields to be transformed to a protobuf message
        while keeping the original data and dataset ids
        """
        adata = await sync_to_async(getattr)(self, "data")
        if adata.get("mode") is not None:
            m = adata.get("mode")
            adata["mode"] = {m["resourcetype"]: {k: m[k] for k in set(list(m.keys())) - set(["resourcetype"])}}
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
        list_serializer_class = getattr(meta, "list_serializer_class", LedPanelListSerializer)
        return list_serializer_class(*args, **list_kwargs)
