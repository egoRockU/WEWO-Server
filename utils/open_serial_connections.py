def open_serial_connections(serial, name):
    try:
        serial.open()
        print(f"{name} Connection Success!")
        return True
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        return False