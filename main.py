from flask import Flask, render_template, request
from serial import Serial
import time
import threading
from threading import Lock
from flask_apscheduler import APScheduler

from utils.open_serial_connections import open_serial_connections
#from utils.object_detection import pi_capture_image, identify_bottle
from utils.db_queries import insert_collected_bottles, insert_turbidity, get_pumper_values

import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2

# INITIAL SETUPS
VENDO_SERIAL = "/dev/ttyACM0"
FILTER_SERIAL = "/dev/ttyUSB0"
# DATABASE_PATH = "/db/database.db"

app = Flask(__name__)
scheduler = APScheduler()

# VENDO SERIAL CONNECTION
vendo_ser = Serial()
vendo_ser.baudrate = 115200
vendo_ser.port = VENDO_SERIAL
vendo_ser.timeout = 1

# FILTER SERIAL CONNECTION
filter_ser = Serial()
filter_ser.baudrate = 9600
filter_ser.port = FILTER_SERIAL
filter_ser.timeout = 1

data_buffer = []
buffer_lock = Lock()


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/serial-send-filter', methods=['POST'])
def serial_send_filter():
    data = request.form
    message = data['message']
    print(message)
    res = "res: " + message + "\n"
    if filter_ser.is_open:
        print("Sent: " + message)
        filter_ser.write(res.encode())
        # is_done = False
        # while not is_done:
        #     if filter_ser.in_waiting:
        #         print("here")
        #         data = filter_ser.readline().decode('utf8').strip()
        #         print(data)
        #         is_done = True
    else: 
        print("Sending Failed")
    return render_template('home.html')


def vendo_serial_listen():
    global data_buffer
    time.sleep(5)

    if (open_serial_connections(vendo_ser, "Vendo") == False):
        return
   
    while True:
        if vendo_ser.in_waiting:
            data = vendo_ser.readline().decode('utf8').strip()
            if 'OBJECT DETECTED!' in data:
                image_arr = pi_capture_image()
                if image_arr is None:
                    data_buffer.append('Camera did not work properly')
                    res = "res: " + str(4) + "\n"
                    vendo_ser.write(res.encode())
                    print(data_buffer)
                else:
                    bottle_class = identify_bottle(image_arr)
                    if bottle_class is None:
                        print("Not bottle")
                        with buffer_lock:
                            data_buffer.append("Not Bottle")
                            res = "res: " + str(3) + "\n"
                            print(res)
                            vendo_ser.write(res.encode())
                            print(data_buffer)
                    else:
                        print("bottle class: ", bottle_class)
                        with buffer_lock:
                            data_buffer.append(bottle_class)
                            res = "res: " + str(bottle_class) + "\n"
                            vendo_ser.write(res.encode())
                            print(data_buffer)
            
            if 'TOTAL LITERS:' in data:
                liters = int(data.split(':')[-1].strip())
                res = "res: " + str(liters) + "\n"
                filter_ser.write(res.encode())
                
                large = 0
                medium = 0
                small = 0
                for data in data_buffer:
                    if data == 0:
                        large += 1
                    if data == 1:
                        medium += 1
                    if data == 2:
                        small += 1

                insert_collected_bottles(small, medium, large, liters) #This is where saving bottles in db happen
                data_buffer = []

            if isinstance(data, str) and 'req: check pumper values' in data.lower():
                pumper_values = get_pumper_values()
                if isinstance(pumper_values, list):
                    res = f'''res: Large: {pumper_values[2]['value']} | Medium: {pumper_values[1]['value']} | Small: {pumper_values[0]['value']}\n'''
                    print("Pumper Values has been sent successfully.")
                else:
                    res = pumper_values
                vendo_ser.write(res.encode())

            if isinstance(data, str) and 'req: check tank 3' in data.lower():
                with buffer_lock:
                    if filter_ser.is_open:
                        is_done = False
                        res = "res: Check Water Level\n"
                        filter_ser.write(res.encode())
                        while not is_done:
                            if filter_ser.in_waiting:
                                filter_data = filter_ser.readline().decode('utf8').strip()
                                index = filter_data.lower().find("res:") + len("res: ")
                                is_tank3_empty = filter_data[index:]
                                res = 'res: ' + is_tank3_empty + "\n"
                                vendo_ser.write(res.encode())
                                is_done = True
                    else:
                        print("Filter Serial is not Open")


def filter_serial_listen():
    time.sleep(5)

    if (open_serial_connections(filter_ser, "Filter") == False):
        return
    
    # while True:
    #     if filter_ser.in_waiting:
    #         data = filter_ser.readline().decode('utf8').strip()
    #         print(data)


# this is where object detection functions declare originally
# remove this comment if it works     

def pi_capture_image():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(
        main={"size": (640, 640), "format": "RGB888"}, 
        )
    picam2.configure(camera_config)

    picam2.start()
    time.sleep(2)
    frame = picam2.capture_array()
    picam2.close()
    
    return frame

def identify_bottle(image_array):
    yolo_model = "models/1.3kSetAug.pt"
    cls_list = ["Large", "Medium", "Small"]

    model = YOLO(yolo_model)

    results = model(source=image_array)

    if (len(results[0]) == 0):
        return None

    result = results[0].boxes.cpu().numpy()
    print("Result: ", result.cls[0])
    object_cls = int(result.cls[0])

    return object_cls


def check_water_quality():
    if filter_ser.is_open:
        message = "Sent: check water quality\n"
        filter_ser.write(message.encode())
        # is_done = False
        # while not is_done:
        #     if filter_ser.in_waiting:
        #         data = filter_ser.readline().decode('utf8').strip()
        #         index = data.find("Turbidity:") + len("Turbidity: ")
        #         turbidity_value = int(data[index:])
        #         insert_turbidity(turbidity_value) # this saves the turbidity to the db
        #         is_done = True
    else:
        print("Filter Serial is not open")

if __name__ == '__main__':
    # Start the serial listener thread
    vendo_listener_thread = threading.Thread(target=vendo_serial_listen, daemon=True)
    filter_listener_thread = threading.Thread(target=filter_serial_listen, daemon=True)
    vendo_listener_thread.start()
    filter_listener_thread.start()
    scheduler.add_job(id="Water Checking Scheduled Task", func=check_water_quality, trigger='interval', minutes=1)
    scheduler.start()

    # Run the Flask app
    app.run(threaded=True)