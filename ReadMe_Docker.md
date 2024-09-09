## Docker Compose Guide

## Prerequisites

- [Docker installed](https://docs.docker.com/engine/install/ubuntu/).

## Getting Started

1. **Navigate to your project directory** where the `docker-compose.yml` file is located.

2. **Build project** 
    ```bash
    docker-compose build
    ```

3. **Start docker** 
    ```bash
    docker-compose up -d
    ```

4. **Add migrations** 
    ```bash
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    ```

4. **Add super User** 
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    user: admin    
    Password: admin

3. **Stop docker** 
    ```bash
    docker-compose down
    ```

## Common Commands

### Up and Running

- **Start services in the background** (detached mode):
  ```bash
  docker-compose up -d
  ```

- **Start services in the foreground** (logs displayed in the terminal):
  ```bash
  docker-compose up
  ```

- **Start specific services**:
  ```bash
  docker-compose up <docker-container>
  ```
  ex: docker-compose logs web

### Stopping Services

- **Stop running services**:
  ```bash
  docker-compose down
  ```

- **Stop services but keep the containers**:
  ```bash
  docker-compose stop
  ```

### Managing Containers

- **List running containers**:
  ```bash
  docker-compose ps
  ```

- **View logs for all services**:
  ```bash
  docker-compose logs
  ```

- **View logs for a specific service**:
  ```bash
  docker-compose logs <docker-container>
  ```

- **Execute a command in a running container**:
  ```bash
  docker-compose exec <docker-container> <command>
  ```

### Building Images

- **Build or rebuild services**:
  ```bash
  docker-compose build
  ```

- **Force rebuild without cache**:
  ```bash
  docker-compose build --no-cache
  ```

### Other Useful Commands

- **Remove stopped service containers**:
  ```bash
  docker-compose rm
  ```

- **View Docker Compose version**:
  ```bash
  docker-compose --version
  ```

### List of the container in IOT Controller Project
- db 
- web 
- celery
- redis
- grpc_server
