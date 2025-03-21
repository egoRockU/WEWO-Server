# WEWO SERVER

This is the official machine server for WEWO, built using [Flask](https://flask.palletsprojects.com/en/stable/). The server run through a microprocessor ([Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)) and is used for complex processes which includes communicating to the machine's microcontrollers ([ESP32](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf), and [Gizduino Atmega644](https://www.e-gizmo.net/gizmoshop/index.php?route=product/product&product_id=489)), object detection using [YOLOv11](https://docs.ultralytics.com/models/yolo11/), chaching of data using [SQLite](https://www.sqlite.org/), and serves as an API endpoint for data that is being fetched by the [wewo website](https://wewo-website.vercel.app/).

### Getting Started

Run the server locally by following the steps bellow:

#### Prerequisites

Ensure you have the following installed:
 - Latest [Python3](https://www.python.org/downloads/) with [pip](https://pypi.org/project/pip/) as package installer.

#### Installation

1. Clone the repository:
```git clone https://github.com/egoRockU/WEWO-Server```
2. Setup python virtual environment:
```python3 -m venv env```
```source env/bin/activate```
3. Install dependencies:
```pip install flask numpy ultralytics picamera2 pyserial requests```
> [!WARNING]
> Due to some libraries not installing properly on Rapsberry Pi OS, we opt to install libraries as system-wide Python packages. However, if you use other OS, pip might be enough to install all required libraries. 
> Bellow are the following instructions for how we actually installed dependency.

```sudo apt install python3-flask python3-numpy python3-ultralytics python3-picamera2 python3-pyserial python3-requests```

4. Start development server:
```python3 main.py```

### Deployment

In order for website to access the API endpoints you have to somehow expose the server to the internet.
You can do this using the following options:
- [Port Forwarding](https://en.wikipedia.org/wiki/Port_forwarding)
- [Network Tunneling](https://www.cloudflare.com/learning/network-layer/what-is-tunneling/)

We did the network tunneling method using [ngrok](https://ngrok.com/), unfortunately we cannot include the steps for deploying using our own domain for security reasons. For that, we recommend you to visit [Learn More](https://ngrok.com/docs).