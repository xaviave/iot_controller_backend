import logging
import threading

import grpc
from django_socio_grpc import generics


class IotMixin(generics.AsyncModelService):
    @staticmethod
    def _grpc_request(stub_class, request):
        # ip should be specific to the product
        with grpc.insecure_channel("10.6.6.6:50051") as channel:
            stub = stub_class(channel)
            try:
                # We only want to update the IOT product
                # Maybe in the future a http message
                response = stub.Update(request)
                print(response)
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

    def grpc_request(self, stub_class, request):
        t = threading.Thread(target=self._grpc_request, args=[stub_class, request], daemon=True)
        t.start()
