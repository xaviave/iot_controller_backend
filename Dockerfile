# Use an official Python runtime as a parent image
FROM python:3.12-slim

RUN apt update && \
    apt install -y \
    gcc \
    openssl \
    rabbitmq-server \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpq-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /iot_controller_backend

# Copy the rest of the application code into the container
COPY . /iot_controller_backend/

# Copy the entire requirements directory into the container
RUN pip install --no-cache-dir uv
RUN uv pip install --no-cache-dir -r requirements/requirements_dev.txt --system
