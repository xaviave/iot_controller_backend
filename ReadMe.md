<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->
<!-- https://derlin.github.io/bitdowntoc/() -->

<!-- TOC --><a name="iot-controller"></a>

# IOT controller

- [Summary](#summary)
- [Model Architecture](#model-architecture)
	* [Products](#products)
	* [Tasks](#tasks)
	* [Error messages](#error-messages)
- [To-Do](#to-do)
- [Installation and development commands](#installation-and-development-commands)
	* [Installation](#installation)
		+ [Global settings](#global-settings)
		+ [PostgreSQL](#postgresql)
		+ [Python libraries](#python-libraries)
	* [Development commands](#development-commands)
		+ [Linter](#linter)
		+ [Update gRPC ](#update-grpc)
	* [Local network settings](#local-network-settings)
		+ [Django Service Setup](#django-service-setup)
	* [Celery and Broker](#celery-and-broker)
		+ [Celery Service Setup](#celery-service-setup)

<!-- TOC end -->

<!-- TOC --><a name="summary"></a>

## Summary

Control and manage IOT products from a Django server (Raspberry PI) thanks to a gRPC (REST like) API.\
Each product are store in Postgres DB with different models and functionality over a polymorphic model
architecture allowing a lot of
abstraction.\
Products are control over a gRPC protocol allowing a free ecosystem of FW on edge.\
This project aim to be a server without frontend and controlled via gRPC from an app.\
The Django admin is use as a frontend if needed.

<!-- TOC --><a name="model-architecture"></a>

## Model Architecture

<!-- TOC --><a name="products"></a>

### Products

A `BaseProduct` model is used as the mother of all products with all basic functionalities.

- Led, low level control of a LED product, from strips to panel.\
  Describe the status, different modes to control the light and the brightness.
- Coffee machine, control the motors and monitor the machine sensors.
  Describe the status, different modes to control the motors.

<!-- TOC --><a name="tasks"></a>

### Tasks

The Celery task are used to send programmed commands to the Products via rules set from the App or the Admin
view.\
Can be use to auto-start products, execute task on following User specified rules.

<!-- TOC --><a name="error-messages"></a>

### Error messages

/!\ Not implemented anymore, need to implement in a protobuf model.
Message will be shown to users from the Django's message middleware.
Different message's tags allow custom interaction and frontend display.

    messages.error(request, "UNIMPLEMENTED")

<!-- TOC --><a name="to-do"></a>

## To-Do

- Celery task.
- use always open stub for channel while on product page (stop after 5min of no usage)
- Add [color modes](https://fastled.io/docs/group___color_utils.html)
- Allow user with rights (not just owner) to use a product/project.
- Add auth over gRPC.
- Add gRPC message protocol for errors or warning from the IOT product.
- Add stream communication between django server and IOT following an app request (video or sound stream).

  Describe the status, different modes to control the light and the brightness.

<!-- TOC --><a name="installation-and-development-commands"></a>

## Installation and development commands

<!-- TOC --><a name="installation"></a>

### Installation

<!-- TOC --><a name="global-settings"></a>

#### Global settings

Linux libraries to install:

```sh
sudo apt-get update && sudo apt upgrade
sudo apt install openssl rabbitmq-server
sudo apt -y install python3-pip libpq-dev postgresql postgresql-contrib
```

---
<!-- TOC --><a name="postgresql"></a>

#### PostgreSQL

Start PostgreSQL service.

```sh
sudo service postgresql start
sudo -u postgres psql
```

It will open a PostgreSQL prompt where you will create your user and the database.\
Don't forget to update the user and password when pasting it in the prompt.

```sql
CREATE ROLE gmx;
CREATE
DATABASE led_controller_db;
ALTER
USER gmx WITH PASSWORD '1234';
ALTER
ROLE gmx WITH LOGIN;
ALTER
ROLE gmx WITH CREATEDB;
ALTER
ROLE gmx SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE
led_controller_db TO gmx;
ALTER
DATABASE led_controller_db OWNER TO gmx;
\q
```

An env var is set with the PostgreSQL Database IP like this:

```sh
DATABASE_URL=psql://<user>:<password>@<ip>:<port>/<database_name>
# example from the sql command:
DATABASE_URL=psql://gmx:1234@127.0.0.1:5432/led_controller_db
```

You can now access without admin user to the database:
```sh
# psql -U <user> <db>
psql -U gmx led_controller_db
```
---
<!-- TOC --><a name="python-libraries"></a>

#### Python libraries

Let's install all the python requirements, see [uv](https://github.com/astral-sh/uv)

```sh
uv python install 3.12
uv venv --python 3.12
source .venv/bin/activate

pip3 install uv
uv pip sync requirements/requirements_base.txt
uv pip install requirements/requirements_base.txt
```

Export the env variables for the project.\
Launch these commands once and the site is initialised.

```sh
source .venv/bin/activate
set -a && . env/.env && set +a
python3 srcs/manage.py makemigrations
python3 srcs/manage.py migrate
python3 srcs/manage.py createsuperuser
```

Then launch the gRPC server to enable the API and app-server-product communication

```sh
set -a && . env/.env && set +a
# Server with gRPC API
python3 srcs manage.py grpcrunaioserver "[::]:50052"
```

*The file `startup_grpc.sh` can be use to update the Python libraries and start the gRPC API.\
Is used by the service command to automatically start the gRPC API on boot.*

To enable the django admin panel

```sh
set -a && . env/.env && set +a
python3 srcs manage.py runserver "0.0.0.0:8000"
```

*The file `startup_admin.sh` can be use to update the Python libraries and start the Admin panel.\
Is used by the service command to automatically start the Admin panel on boot.*

---
<!-- TOC --><a name="development-commands"></a>

### Development commands

<!-- TOC --><a name="linter"></a>

#### Linter

```sh
uv run ruff check --fix
# or
ruff format . && ruff check --select I --fix . && ruff check . --fix
```

<!-- TOC --><a name="update-grpc"></a>

#### Update gRPC

Generate the gRPC files from srcs:

```sh
python3 manage.py generateproto --directory features/products_controller/grpc
```

main diff is the handling of the base_product
We replace the BaseProductRequest and BaseProductResponse to use the Oneof
instead of the mother class of the inheritance.

Steps:

1. Replace the BaseProductRequest, LedModeRequest and BaseProductResponse, LedModeResponse from the
   file `products_controller.proto` by the classes from `tes_polymorphism.proto`
2. Generate the pb2 file with this change from iot_controller_backend/srcs:
   ```sh
   python3 -m grpc_tools.protoc  -I=.  features/products_controller/grpc/products_controller.proto  --python_out=. --grpc_python_out=. --experimental_allow_proto3_optional
   ```

---
<!-- TOC --><a name="local-network-settings"></a>

### Local network settings

if you want a custom namespace, add to `ALLOWED_HOSTS` the name of this namespace.
To allow the server on local network, add your IP address to `ALLOWED_HOST`
in `srcs/base_app/settings.py` like:

    ALLOWED_HOSTS = ['mywebsite.local', 'YOUR_IP']

Launch this command:

```sh
sudo apt install ufw
```

[//]: # (In `/etc/dnsmasq.conf`, add:)

[//]: # (`address=/mywebsite.local/192.168.1.2`)

[//]: # (sudo service dnsmasq restart)

Then:

```sh
sudo ufw 8000/tcp
sudo ufw allow ssh
sudo ufw enable
# Apply your changes and restart the server
reboot
python manage.py runserver 0.0.0.0:8000
```

---
<!-- TOC --><a name="django-service-setup"></a>

#### Django Service Setup

Systemd will allow you to automate the start of your app on boot or when you start the service.

1. **Create a Django service file**\
   Create a new file with the extension `.service` in the `/etc/systemd/system/` directory.\
   Example: `service/django_server.service` for admin panel and `service/django_grpc.service` for gRPC API.
2. **Define the Django service**\
   Define the service using the following syntax:
   ```service
   [Unit]
   Description=Django Web Server

   [Service]
   User=<user>
   Group=<group>
   WorkingDirectory=<path_to_project_directory>
   ExecStart=<path_to_python_executable> <path_to_manage_py> runserver <ip_address>:<port>

   [Install]
   WantedBy=multi-user.target
   ```

   > - *Replace `<user>` and `<group>` with the user and group that will run the Django service.*
   > - *Replace `<path_to_project_directory>` with the path to your Django project directory.*
   > - *Replace `<path_to_python_executable>` with the path to the Python executable (
	   e.g., `/usr/bin/python3`).*
   > - *Replace `<path_to_manage_py>` with the path to the `manage.py` file in your Django project directory.*
   > - *Replace `<ip_address>` and `<port>` with the IP address and port (e.g., `0.0.0.0:8000`).*

3. **Reload the systemd daemon:**\
   Run the following command to reload the systemd daemon and load the new service file
    ```sh
    sudo systemctl daemon-reload
    sudo systemctl start django_server
    sudo systemctl status django_server
    ```

4. **Enable the Django service:**\
   Start automatically when the system boots up, use the following command
    ```sh
    sudo systemctl enable django_server
    ```

---
<!-- TOC --><a name="celery-and-broker"></a>

### Celery and Broker

<!-- TOC --><a name="celery-service-setup"></a>

#### Handle Celery
Start in terminal: `celery -A proj worker -l INFO`\
Start Celery in the background: `celery multi start w1 -A proj -l INFO`\
Wait the tasks to be executed and Stop Celery:\
`celery multi stopwait w1 -A proj -l INFO`

#### Celery Service Setup

1. **Create a Celery service file:**\
   Create a new file with the extension `.service` in the `/etc/systemd/system/` directory. For example, you
   could use `django_celery.service`.

2. **Define the Celery service:**\
   ```sh
   [Unit]
   Description=Celery Worker

   [Service]
   User=<user>
   Group=<group>
   WorkingDirectory=<path_to_project_directory>
   ExecStart=<path_to_python_executable> <path_to_celery_executable> -A <your_celery_project_name> worker --loglevel=info

   [Install]
   WantedBy=multi-user.target
   ```

3. **Reload the systemd daemon:**\
   Run the following command to reload the systemd daemon and load the new service file
    ```sh
    sudo systemctl daemon-reload
    sudo systemctl start django_celery
    sudo systemctl status django_celery
    ```

4. **Enable the Django service:**\
   Start automatically when the system boots up, use the following command
    ```sh
    sudo systemctl enable django_celery
    ```
