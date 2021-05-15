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

    def get(self):
        val = int(self.hx.get_weight(5) * -1)

        return val

    def weight(self):
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(40)
        self.hx.reset()
        self.hx.tare()

        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)
        val = 0
        while val == 0:
            val = self.get()
            time.sleep(10)

        weight_list = []
        cnt = 3
        for i in range(cnt):
            val = self.get()
            if val == 0:
                break
            weight_list.append(val)
            time.sleep(10)

        weight = sum(weight_list) / cnt

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
