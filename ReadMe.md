# IOT controller

Control and manage IOT products from a Django server (Raspberry PI) thanks to a gRPC (REST like) API.

Each product are store in DB with different models and functionality over a polymorphic DB allowing a lot of
abstraction.

Products are control over a gRPC protocol allowing a free ecosystem of FW on edge.

## Products

- Led, low level control of a LED product, from strips to panel.
- Coffee machine, sending command to a controller app handling low level controls.

## Error handling through messages

/!\ Not implemented anymore, need to implement in a protobuf model.
Message will be shown to users from the Django's message middleware.
Different message's tags allow custom interaction and frontend display.

    messages.error(request, "UNIMPLEMENTED")

## To-Do

- Add per product IP and port.
- Allow user with rights (not just owner) to use a product/project.
- Add auth over gRPC.
- Add gRPC message protocol for errors or warning from the IOT product.
- Use always open stub for channel while on product page (stop after 5min of no usage)
- Add [color modes function](https://fastled.io/docs/group___color_utils.html)
- Add stream communication between django server and IOT following a app request (video or sound stream).

## Linter

    ruff format . && ruff check --select I --fix . && ruff check . --fix


## Install command

### Global settings

    sudo apt-get update && sudo apt upgrade
    sudo apt install openssl
    sudo apt -y install python3-pip libpq-dev postgresql postgresql-contrib
    sudo service postgresql start

Then in postgresql create your user and the database

Launch this command: `sudo -u postgres psql`

the env var is like this `DATABASE_URL=psql://gmx:1234@127.0.0.1:5432/led_controller_db`
so adapt your psql command with the right variable

    CREATE ROLE gmx;
    CREATE DATABASE led_controller_db;
    ALTER USER gmx WITH PASSWORD '1234';
    ALTER ROLE gmx WITH LOGIN;
    ALTER ROLE gmx WITH CREATEDB;
    ALTER ROLE gmx SET default_transaction_isolation TO 'read committed';
    GRANT ALL PRIVILEGES ON DATABASE led_controller_db TO gmx;
    ALTER DATABASE led_controller_db OWNER TO gmx;
    \q

Let's install all the python requirements

    python3 -m pip install --upgrade pip
    pip3 install -r requirements/requirements_base.txt

Generate the gRPC files from srcs:

     python3 manage.py generateproto --directory features/products_controller/grpc

Export the env variables for the project

    set -a && . env/.env && set +a

Then simply launch these commands once and the site is initialised

    python3 srcs/manage.py makemigrations
    python3 srcs/manage.py migrate
    python3 srcs/manage.py createsuperuser

[//]: # "    python3 srcs/manage.py loaddata fixtures/base_fixture.json"

Then launch the server

    # Admin without gRPC API
    python3 srcs manage.py runserver
    # Server with gRPC API
    python3 srcs manage.py grpcrunaioserver

---

### Local network settings

if you want a custom namespace, add to `ALLOWED_HOSTS` the name of this namespace.
To allow the server on local network, add your IP address to `ALLOWED_HOST`
in `srcs/base_app/settings.py` like:

    ALLOWED_HOSTS = ['mywebsite.local', 'YOUR_IP']

Launch this command:

    sudo apt install ufw dnsmasq

In `/etc/dnsmasq.conf`, add:

    address=/mywebsite.local/192.168.1.2

Then:

      sudo service dnsmasq restart
      sudo ufw 8000/tcp
      sudo ufw enable
      python manage.py runserver 0.0.0.0:8000

# Django and Celery System Service Setup Guide

## Prerequisites

- A Linux server running a version of systemd (most modern distributions include systemd by default)
- Python installed on the server
- A Django project that you want to run as a system service
- Celery installed in your Django project

## Django Service Setup

1. **Create a Django service file:**

   Create a new file with the extension `.service` in the `/etc/systemd/system/` directory. For example, you
   could use `django.service`.

2. **Define the Django service:**

   Inside the service file, define the service using the following syntax:

   ```sh
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

   - Replace `<user>` and `<group>` with the user and group that will run the Django service.
   - Replace `<path_to_project_directory>` with the path to your Django project directory.
   - Replace `<path_to_python_executable>` with the path to the Python executable (e.g., `/usr/bin/python3`).
   - Replace `<path_to_manage_py>` with the path to the `manage.py` file in your Django project directory.
   - Replace `<ip_address>` and `<port>` with the IP address and port (e.g., `0.0.0.0:8000`).

3. **Reload the systemd daemon:**

   Run the following command to reload the systemd daemon and load the new service file:

<<<<<<< Updated upstream
    ```sh
    sudo systemctl daemon-reload
    sudo systemctl start django_server
    sudo systemctl status django_server
    ```
=======
   ```sh
   sudo systemctl daemon-reload
   sudo systemctl start django
   sudo systemctl status django
   ```
>>>>>>> Stashed changes

4. **Enable the Django service:**

   If you want the service to start automatically when the system boots up, use the following command:

<<<<<<< Updated upstream
    ```sh
    sudo systemctl enable django_server
    ```
=======
   ```sh
   sudo systemctl enable django
   ```
>>>>>>> Stashed changes

## Celery Service Setup

1. **Create a Celery service file:**

   Create a new file with the extension `.service` in the `/etc/systemd/system/` directory. For example, you
   could use `celery.service`.

2. **Define the Celery service:**

   Inside the service file, define the service using the following syntax:

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

3. **Reload the systemd daemon:**

   Run the following command to reload the systemd daemon and load the new service file:

   ```sh
   sudo systemctl daemon-reload
   sudo systemctl start celery
   sudo systemctl status celery
   sudo systemctl enable celery
   ```
