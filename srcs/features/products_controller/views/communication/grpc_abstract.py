import grpc
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from features.products_controller.models.products.base_product import BaseProduct
from grpc_iot import grpc_utils


class GrpcView(View):
    @staticmethod
    def _check_request(request):
        raise NotImplementedError

    @staticmethod
    def _update_object(request, product, **kwargs) -> bool:
        raise NotImplementedError

    @staticmethod
    def _get_grpc_cmds(product) -> list[dict]:
        raise NotImplementedError

    @staticmethod
    def grpc_request(request, product: BaseProduct, grpc_cmds: list[dict]):
        with grpc.insecure_channel("[::]:50051") as channel:
            stub = product.get_stub(channel)
            for cmd in grpc_cmds:
                try:
                    grpc_utils.grpc_setter_cmd(stub, product.get_proto_lib, **cmd)
                except grpc.RpcError as rpc_error:
                    if rpc_error.code() == grpc.StatusCode.CANCELLED:
                        messages.error(request, "Request to product CANCELLED")
                    elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                        messages.error(request, "Product UNAVAILABLE, please check connection")
                    elif rpc_error.code() == grpc.StatusCode.UNIMPLEMENTED:
                        messages.error(request, "Request UNIMPLEMENTED")
                    else:
                        messages.error(
                            request,
                            f"Received unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}",
                        )

    def post(self, request, *args, **kwargs):
        if self._check_request(request):
            product = BaseProduct.objects.get(pk=kwargs["pk"])
            if self._update_object(request, product, **kwargs):
                print(self._get_grpc_cmds(product))
                self.grpc_request(request, product, self._get_grpc_cmds(product))
        return redirect(request.META.get("HTTP_REFERER"))
