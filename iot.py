import time
import RPi.GPIO as GPIO
import numpy as np
from picamera import PiCamera
from io import BytesIO
from PIL import Image

from hx711 import HX711

class Weight():
    def __init__(self):
        self.hx = HX711(21, 20) #DAT CLK

    def weight(self):
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(1)
        self.hx.reset()
        self.hx.tare()

        val = self.hx.get_weight(5)
        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)
        GPIO.cleanup()

        return val

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
