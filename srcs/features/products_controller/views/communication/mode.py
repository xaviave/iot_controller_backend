from django.contrib import messages
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.views.communication.grpc_abstract import GrpcView


class ModeView(GrpcView):
    @staticmethod
    def _check_request(request):
        return "set_mode" in request.POST or "set_save_mode" in request.POST

    @staticmethod
    def _update_object(request, product, **kwargs) -> bool:
        if isinstance(product, LedPanel):
            if "set_save_mode" in request.POST:
                requested_mode = LedMode.__subclasses__()[LedMode.mode_names().index(kwargs["mode"])]
                form = requested_mode.get_form()(request.POST, request.FILES)
                if not form.is_valid():
                    messages.error(
                        request,
                        # todo: better print and error handling
                        f"Error in form, {list(form.errors.values())[0][0]}",
                    )
                    return False
                # todo: add to model the kwargs["value"] = tmp | save
                product.mode = form.save()
            elif "set_mode" in request.POST:
                product.mode = LedMode.objects.get(pk=kwargs["mode_pk"])
        else:
            product.mode_value = int(kwargs["mode"])
        product.save()
        return True

    @staticmethod
    def _get_grpc_cmds(product) -> list[dict]:
        """
        Generate a list of request that will be sent together
        Command's order is important
        """
        cmds = []
        if product.mode.has_mode:
            cmds.append(product.mode.get_grpc_cmd())
        cmds.append({"fn_name": "SetMode", "class_name": "Mode", "mode": product.grpc_mode_value})
        return cmds
