## Docker Compose Guide

## Getting Started

Follow guide: https://medium.com/@tommyraspati/monitoring-your-django-project-with-prometheus-and-grafana-b06a5ca78744

When you add data the URL is not http://localhost:9090 but the URL of the Network app-network

Just do:
- docker network inspect iot_controller_backend_app-network

Find the line: "Gateway": The IP adress. for me:
- "172.18.0.1"

Add in prometheus server URL:
http://Your-addres:9090/


