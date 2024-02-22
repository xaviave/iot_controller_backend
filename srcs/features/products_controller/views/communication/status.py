from features.products_controller.models.status import Status
from features.products_controller.views.communication.grpc_abstract import GrpcView


class StatusView(GrpcView):
    @staticmethod
    def _check_request(request):
        return "set_status" in request.POST

    @staticmethod
    def _update_object(request, product, **kwargs) -> bool:
        product.status = getattr(Status, kwargs["status"])
        product.save()
        return True

    @staticmethod
    def _get_grpc_cmds(product) -> list[dict]:
        return [{"fn_name": "SetStatus", "class_name": "Status", "state": product.get_status()}]
