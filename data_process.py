import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import time
import statistics
import requests
from picamera import PiCamera
from io import BytesIO
from PIL import Image

def make_dict(name1='color', val1='123', name2='eat', val2='123'):
    dict = {
        name1 : val1,
        name2 : val2
    }
    return dict

class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)

    def capture(self):
        self.camera.start_preview()
        stream = BytesIO()
        sleep(2)

        self.camera.capture(stream, 'jpeg')
        img = Image.open(stream)
        img = np.array(img)

        return img

class Parcing():
    def __init__(self):
        self.cluster = 4

    def restroom(self, img):
        flat_image = np.reshape(img, [-1, 3])

        # segmentation
        kmeans = KMeans(n_clusters=self.cluster)
        kmeans.fit(flat_image)
        labels = kmeans.labels_
        labels = np.reshape(labels,img.shape[:2])
        # plt.imshow(labels)
        # plt.show()

        # extract color
        color_list = []
        for n in range(self.cluster):
            val = img[np.where(labels == n)].mean(axis=0)
            color_list.append(np.array(val))
        # print(color_list)

        # compare color with white
        cnt = 0
        dist = -10000
        white = np.array([255, 255, 255])
        yellow = np.array([237, 207, 33])
        for n in range(self.cluster):
            val = np.linalg.norm(color_list[n] - white) - np.linalg.norm(color_list[n] - yellow)
            # print(color_list[n])
            # print(val)
            if val > dist:
                dist = val
                cnt = n

        color = color_list[cnt]
        # plt.imshow(np.tile(color / 255, (100, 100, 1)))
        # plt.show()
        return color

    def restaurant(self, weight_list):
        before_weight = 0
        median_weight = 0
        max_weight = 0
        min_weight = 0
        food = 0

        for i in range(len(weight_list)):
            median_weight = statistics.median(weight_list)
            max_weight = max(weight_list)
            min_weight = min(weight_list)
            food = max_weight - min_weight

            if (food > median_weight * 3):
                weight_list.remove(max_weight)
            else:
                break

        return food

    def send_json(self, data):
        URL = 'http://13.209.18.94:3000/users'

        res = requests.post(URL, json=data)
        #print('POST    :', res.status_code)
        #print(res.text)
        return res