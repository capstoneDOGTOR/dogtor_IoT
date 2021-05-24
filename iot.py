import time
import RPi.GPIO as GPIO
import numpy as np
from picamera import PiCamera
from io import BytesIO
from PIL import Image
from collections import Counter

from hx711 import HX711

class Weight():
    def __init__(self):
        self.hx = HX711(21, 20) #DAT CLK

    def start(self):
        print('weight start')
        while(True):
            val = int(self.hx.get_weight(5))
            print(val)

            if val > 20:
                break
            else:
                self.hx.power_down()
                time.sleep(10)
                self.hx.power_up()

        return

    def get(self):
        print('weight get')
        weight_list = []
        while(True):
            val = int(self.hx.get_weight(5))
            print(val)

            if val < 20:
                break
            else:
                weight_list.append(val)
                self.hx.power_down()
                time.sleep(10)
                self.hx.power_up()

        weight = sum(weight_list) / len(weight_list)
        return weight

    def weight(self):
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(25)
        self.hx.reset()
        self.hx.tare()

        self.start()
        weight = self.get()

        GPIO.cleanup()
        return weight

class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)

    def capture(self):
        self.camera.start_preview()
        stream = BytesIO()
        time.sleep(2)

        self.camera.capture(stream, 'jpeg')
        img = Image.open(stream)
        img = np.array(img)

        return img
