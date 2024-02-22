from django.contrib import admin
from django.utils.safestring import mark_safe
from features.products_controller.models.category import Category
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.models.products.led.led_mode import (
    ColorMode,
    ImageMode,
    LedMode,
    PatternMode,
    VideoMode,
)
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.models.project import Project
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
    StackedPolymorphicInline,
)


class LedModeChildAdmin(PolymorphicChildModelAdmin):
    base_model = LedMode


@admin.register(ImageMode)
class ImageModeAdmin(LedModeChildAdmin):
    @staticmethod
    def img_preview(obj):
        return mark_safe(f"<img src='{obj.image.url}' width='200' />")

    @staticmethod
    def img_low_pixel_preview(obj):
        return mark_safe(f"<img src='{obj.image_low_pixel.url}' width='200' />")

    show_in_index = False
    list_display = ("name", "image")
    exclude = ("image_low_pixel",)
    readonly_fields = ("img_preview", "img_low_pixel_preview")


@admin.register(VideoMode)
class VideoModeAdmin(LedModeChildAdmin):
    @staticmethod
    def video_preview(obj):
        return mark_safe(
            f"""
            <div>
                <video controls preload="metadata" width="480" loop="loop" autoplay="autoplay" controls muted>
                    <source src="{obj.video.url}">
                    Your browser does not support the video tag.
                </video>
            </div>
        """
        )

    @staticmethod
    def video_low_pixel_preview(obj):
        return mark_safe(
            f"""
            <div>
                <video controls preload="metadata" width="240" loop="loop" autoplay="autoplay" controls muted>
                    <source src="{obj.video_low_pixel.url}">
                    Your browser does not support the video tag.
                </video>
            </div>
        """
        )

    show_in_index = False
    list_display = ("name", "video")
    exclude = ("video_low_pixel",)
    readonly_fields = ("video_preview",)
    # "video_low_pixel_preview") WIP


@admin.register(ColorMode)
class ColorModeAdmin(LedModeChildAdmin):
    show_in_index = False
    list_display = ("name",)


@admin.register(PatternMode)
class PatternModeAdmin(LedModeChildAdmin):
    show_in_index = False
    list_display = ("name",)


@admin.register(LedMode)
class LedModeAdmin(PolymorphicParentModelAdmin):
    base_model = LedMode
    child_models = (ImageMode, VideoMode, PatternMode, ColorMode)

    def get_mode(self, obj):
        return obj.get_real_concrete_instance_class().__name__

    get_mode.short_description = "Type"
    list_display = ("name", "get_mode")
    list_filter = (
        "name",
        PolymorphicChildModelFilter,
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


class BaseProductChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseProduct


@admin.register(LedPanel)
class LedPanelAdmin(BaseProductChildAdmin):
    show_in_index = False
    list_display = ("name", "show_categories")

    def show_categories(self, obj):
        return [c.name for c in obj.categories.all()]


@admin.register(CoffeeMachine)
class CoffeeMachineAdmin(BaseProductChildAdmin):
    show_in_index = False
    list_display = ("name", "show_categories")

    def show_categories(self, obj):
        return [c.name for c in obj.categories.all()]


@admin.register(BaseProduct)
class BaseProductAdmin(PolymorphicParentModelAdmin):
    base_model = BaseProduct
    child_models = (LedPanel, CoffeeMachine)

    list_display = ("name", "show_categories")
    list_filter = (
        "name",
        PolymorphicChildModelFilter,
    )

    def show_categories(self, obj):
        return [c.name for c in obj.categories.all()]


class CategoryInline(admin.TabularInline):
    base_model = BaseProduct.categories.through


class BaseProductInline(StackedPolymorphicInline):
    class CoffeeMachineInline(StackedPolymorphicInline.Child):
        model = CoffeeMachine

    class LedPanelInline(StackedPolymorphicInline.Child):
        model = LedPanel

    model = Project.products.through
    inlines = (CategoryInline,)
    child_inlines = (LedPanelInline, CoffeeMachineInline)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
