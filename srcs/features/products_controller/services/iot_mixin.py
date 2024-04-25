import logging

import grpc
from django_socio_grpc import generics
from grpcio_iot import grpc_utils


class IotMixin(generics.AsyncModelService):
    @staticmethod
    def grpc_request(stub_class, request):
        print(request)
        # ip should be specific to the product
        with grpc.insecure_channel("[::]:50051") as channel:
            stub = stub_class(channel)
            try:
                # We only want to update the IOT product
                # Maybe in the future a http message
                stub.Update(request)
            except grpc.RpcError as rpc_error:
                if rpc_error.code() == grpc.StatusCode.CANCELLED:
                    logging.error("Request to product CANCELLED")
                elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                    logging.error("Product UNAVAILABLE, please check connection")
                elif rpc_error.code() == grpc.StatusCode.UNIMPLEMENTED:
                    logging.error("Request UNIMPLEMENTED")
                else:
                    logging.error(
                        f"Received unknown RPC error: code={rpc_error.code()} message={rpc_error.details()}",
                    )
