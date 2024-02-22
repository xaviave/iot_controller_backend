pwd
set -a && . env/.env && set +a
/home/gmx/Documents/django_iot_controller/django_venv/bin/python -m pip install -U -r requirements/requirements_dev.txt
/home/gmx/Documents/django_iot_controller/django_venv/bin/python software/server/manage.py migrate
/home/gmx/Documents/django_iot_controller/django_venv/bin/python software/server/manage.py runserver 0.0.0.0:8000
