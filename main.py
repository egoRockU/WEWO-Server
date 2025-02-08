from flask import Flask, render_template, request
from serial import Serial
import time
import threading
from threading import Lock

from utils.open_serial_connections import open_serial_connections
from utils.object_detection import pi_capture_image, identify_bottle
from utils.db_queries import insert_collected_bottles

# INITIAL SETUPS
VENDO_SERIAL = "/dev/ttyACM0"
FILTER_SERIAL = "/dev/ttyUSB0"
DATABASE_PATH = "/db/database.db"

app = Flask(__name__)

# VENDO SERIAL CONNECTION
vendo_ser = Serial()
vendo_ser.baudrate = 115200
vendo_ser.port = VENDO_SERIAL
vendo_ser.timeout = 1

# FILTER SERIAL CONNECTION
filter_ser = Serial()
filter_ser.baudrate = 115200
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
    else: 
        print("Sending Failed")
    return render_template('home.html')


def vendo_serial_listen():
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
                    if data == "Large":
                        large += 1
                    if data == "Medium":
                        medium += 1
                    if data == "Small":
                        small += 1

                insert_collected_bottles(small, medium, large, liters) #This is where saving bottles in db happen
                data_buffer = []

def filter_serial_listen():
    time.sleep(5)

    if (open_serial_connections(filter_ser, "Filter") == False):
        return
    # Add listener functions here if necessary


# this is where object detection functions declare originally
# remove this comment if it works     


if __name__ == '__main__':
    # Start the serial listener thread
    vendo_listener_thread = threading.Thread(target=vendo_serial_listen, daemon=True)
    filter_listener_thread = threading.Thread(target=filter_serial_listen, daemon=True)
    vendo_listener_thread.start()
    filter_listener_thread.start()

    # Run the Flask app
    app.run(threaded=True)