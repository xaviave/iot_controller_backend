from features.products_controller.views.communication.grpc_abstract import GrpcView


class BrightnessView(GrpcView):
    @staticmethod
    def _check_request(request):
        return "set_brightness" in request.POST

    @staticmethod
    def _update_object(request, product, **kwargs) -> bool:
        product.brightness = float(request.POST.get("set_brightness"))
        product.save()
        return True

    @staticmethod
    def _get_grpc_cmds(product) -> list[dict]:
        return [{"fn_name": "SetBrightness", "class_name": "Brightness", "value": product.brightness}]
