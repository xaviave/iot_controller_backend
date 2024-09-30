import logging
import threading

import grpc
from django_socio_grpc import generics


def execute_grpc_request(stub_class, request) -> None:
    # ip should be specific to the product
    with grpc.insecure_channel(f"{request.ip_address}:{request.ip_port}") as channel:
        stub = stub_class(channel)
        try:
            # We only want to update the IOT product
            # Maybe in the future a http debug message
            response = stub.Update(request)
            print(response)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                logging.exception("Request to product CANCELLED")
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logging.exception("Product UNAVAILABLE, please check connection")
            elif rpc_error.code() == grpc.StatusCode.UNIMPLEMENTED:
                logging.exception("Request UNIMPLEMENTED")
            else:
                logging.exception(
                    f"Received unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}",
                )


class IotMixin(generics.AsyncModelService):
    @staticmethod
    def grpc_request(stub_class, request) -> None:
        t = threading.Thread(target=execute_grpc_request, args=[stub_class, request], daemon=True)
        t.start()
