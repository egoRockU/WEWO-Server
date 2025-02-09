from flask import Flask, render_template, request
from serial import Serial
import time
import threading
from threading import Lock
from flask_apscheduler import APScheduler

from utils.open_serial_connections import open_serial_connections
from utils.object_detection import pi_capture_image, identify_bottle
from utils.db_queries import insert_collected_bottles, insert_turbidity, get_pumper_values
from utils.parse_res import parse_res

from endpoint.routes import endpoint

# INITIAL SETUPS
VENDO_SERIAL = "/dev/ttyACM0"
FILTER_SERIAL = "/dev/ttyUSB0"

app = Flask(__name__)
app.register_blueprint(endpoint)
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
    else: 
        print("Sending Failed")
    return render_template('home.html')

@app.route('/test')
def test():
    return 'Hello from WEWO Server'


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
                    res = "class res: " + str(4) + "\n"
                    vendo_ser.write(res.encode())
                    print(data_buffer)
                else:
                    bottle_class = identify_bottle(image_arr)
                    if bottle_class is None:
                        print("Not bottle")
                        with buffer_lock:
                            data_buffer.append("Not Bottle")
                            res = "class res: " + str(3) + "\n"
                            print(res)
                            vendo_ser.write(res.encode())
                            print(data_buffer)
                    else:
                        print("bottle class: ", bottle_class)
                        with buffer_lock:
                            data_buffer.append(bottle_class)
                            res = "class res: " + str(bottle_class) + "\n"
                            vendo_ser.write(res.encode())
                            print(data_buffer)
            
            if 'TOTAL LITERS:' in data:
                liters = int(data.split(':')[-1].strip())
                res = "provide res: " + str(liters) + "\n"
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
                    res = f'''pumper values res: Large: {pumper_values[2]['value']} | Medium: {pumper_values[1]['value']} | Small: {pumper_values[0]['value']}\n'''
                    print("Pumper Values has been sent successfully.")
                else:
                    res = pumper_values
                vendo_ser.write(res.encode())

            if isinstance(data, str) and 'req: check tank 3' in data.lower():
                with buffer_lock:
                    if filter_ser.is_open:
                        res = "res: Check Water Level\n"
                        filter_ser.write(res.encode())
                    else:
                        print("Filter Serial is not Open")


def filter_serial_listen():
    time.sleep(5)

    if (open_serial_connections(filter_ser, "Filter") == False):
        return
    
    while True:
        if filter_ser.in_waiting:
            data = filter_ser.readline().decode('utf8').strip()

            if isinstance(data, str) and 'tank 3 status' in data.lower():
                res = 'tank 3 level res: ' + parse_res(data, 'res:') + "\n"
                vendo_ser.write(res.encode())
                print("Tank 3 Has been checked!")

            if isinstance(data, str) and 'water quality status' in data.lower():
                turbidity_value = int(parse_res(data, "Turbidity:"))
                insert_turbidity(turbidity_value)


def check_water_quality():
    if filter_ser.is_open:
        message = "Sent: check water quality\n"
        filter_ser.write(message.encode())
    else:
        print("Filter Serial is not open")


if __name__ == '__main__':
    vendo_listener_thread = threading.Thread(target=vendo_serial_listen, daemon=True)
    filter_listener_thread = threading.Thread(target=filter_serial_listen, daemon=True)
    vendo_listener_thread.start()
    filter_listener_thread.start()
    scheduler.add_job(id="Water Checking Scheduled Task", func=check_water_quality, trigger='interval', hours=1)
    scheduler.start()

    app.run(threaded=True)