from celery import shared_task
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.services.iot_mixin import execute_grpc_request


@shared_task
def product_set_status(product_id: int):
    p = BaseProduct.objects.get(pk=product_id)
    product_request = p.get_grpc_request()
    stub = p.get_stub()
    execute_grpc_request(stub, product_request)
    print("request sent")
