# WEWO SERVER
---
This is the official machine server for WEWO, built using [Flask](https://flask.palletsprojects.com/en/stable/). The server run through a microprocessor ([Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)) and is used for complex processes which includes communicating to the machine's microcontrollers ([ESP32](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf), and [Gizduino Atmega644](https://www.e-gizmo.net/gizmoshop/index.php?route=product/product&product_id=489)), object detection using [YOLOv11](https://docs.ultralytics.com/models/yolo11/), chaching of data using [SQLite](https://www.sqlite.org/), and serves as an API endpoint for data that is being fetched by the [wewo website](https://wewo-website.vercel.app/).

### Get Started
---
> [!WARNING]
> Due to some libraries not installing properly on Rapsberry Pi OS, we prefer to install libraries as system-wide Python packages. 