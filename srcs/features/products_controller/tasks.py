
from celery import shared_task

# from scapy.all import ARP, Ether, conf, srp
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.services.iot_mixin import execute_grpc_request

"""
from celery.schedules import crontab
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}"""
"""
from celery.schedules import solar
app.conf.beat_schedule = {
    # Executes at sunset in Melbourne
    'add-at-melbourne-sunset': {
        'task': 'tasks.add',
        'schedule': solar('sunset', -37.81753, 144.96715),
        'args': (16, 16),
    },
}
"""


@shared_task
def product_set_status(product_id: int):
    p = BaseProduct.objects.get(pk=product_id)
    product_request = p.get_grpc_request()
    stub = p.get_stub()
    execute_grpc_request(stub, product_request)
    print("request sent")

#
# def check_host_connection(host: str):
#     print("[*] Scanning...")
#     start_time = datetime.now()
#
#     conf.verb = 0
#     ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1/24"), timeout=2, iface="etho0", inter=0.1)
#
#     print("\n[*] IP - MAC")
#     for _snd, rcv in ans:
#         print(rcv.sprintf(r"%ARP.psrc% - %Ether.src%"))
#     stop_time = datetime.now()
#     total_time = stop_time - start_time
#     print("\n[*] Scan Complete. Duration:", total_time)
