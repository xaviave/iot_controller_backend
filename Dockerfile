# Use an official Python runtime as a parent image
FROM python:3.11-slim

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
WORKDIR /srcs

# Copy the entire requirements directory into the container
COPY requirements/ /srcs/requirements/
RUN pip install --no-cache-dir -r requirements/requirements_dev.txt

# Copy the rest of the application code into the container
COPY srcs/ /srcs/

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]