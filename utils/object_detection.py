import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2
import time

def capture_image():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if cap.isOpened():
        frame_count = 0
        while frame_count < 100:
            ret, frame = cap.read()
            frame_array = np.array(frame)
            frame_count += 1
    else:
        return None

    cap.release()
    cv2.destroyAllWindows()

    return frame_array

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
    yolo_model = "./models/1.3kSetAug.pt"
    cls_list = ["Large", "Medium", "Small"]

    model = YOLO(yolo_model)

    results = model(source=image_array, conf=0.7)

    if (len(results[0]) == 0):
        return None

    result = results[0].boxes.cpu().numpy()
    print("Result: ", result.cls[0])
    object_cls = int(result.cls[0])

    return object_cls