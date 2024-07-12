from datetime import datetime

from celery import shared_task
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.services.iot_mixin import execute_grpc_request
from scapy.all import ARP, Ether, conf, srp


@shared_task
def product_set_status(product_id: int):
    p = BaseProduct.objects.get(pk=product_id)
    product_request = p.get_grpc_request()
    stub = p.get_stub()
    execute_grpc_request(stub, product_request)
    print("request sent")


def check_host_connection(host: str):
    print("[*] Scanning...")
    start_time = datetime.now()

    conf.verb = 0
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1/24"), timeout=2, iface="etho0", inter=0.1)

    print("\n[*] IP - MAC")
    for snd, rcv in ans:
        print(rcv.sprintf(r"%ARP.psrc% - %Ether.src%"))
    stop_time = datetime.now()
    total_time = stop_time - start_time
    print("\n[*] Scan Complete. Duration:", total_time)
