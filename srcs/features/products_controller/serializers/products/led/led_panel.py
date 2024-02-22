# serializers.py
from features.products_controller.models.products.led.led_panel import LedPanel
from rest_framework import serializers


class LedPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedPanel
        fields = "__all__"
