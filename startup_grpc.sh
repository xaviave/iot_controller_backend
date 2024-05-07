set -a && . env/.env && set +a
/home/gmx/Documents/iot_controller/venv/bin/python -m pip install -U -r requirements/requirements_dev.txt
# /home/gmx/Documents/iot_controller/venv/bin/python srcs/manage.py migrate
/home/gmx/Documents/iot_controller/venv/bin/python srcs/manage.py grpcrunaioserver 0.0.0.0:50052
