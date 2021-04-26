import numpy as np
import cv2
#import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import time
import statistics
import requests
from picamera import PiCamera
from io import BytesIO
from PIL import Image

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

class Parcing():
    def __init__(self, uid):
        self.cluster = 5
        self.uid = uid

    def hsv2rgb(self, hsv):
        h = hsv[0] * 2
        s = hsv[1] / 255
        v = hsv[2] / 255
        r_ = 0
        g_ = 0
        b_ = 0

        c = v * s
        h_ = h / 60
        x = c * (1 - abs(h_ % 2 - 1))
        if h_ >= 0 and h_ <= 1:
            r_, g_, b_ = c, x, 0
        elif h_ >= 1 and h_ <= 2:
            r_, g_, b_ = x, c, 0
        elif h_ >= 2 and h_ <= 3:
            r_, g_, b_ = 0, c, x
        elif h_ >= 3 and h_ <= 4:
            r_, g_, b_ = 0, x, c
        elif h_ >= 4 and h_ <= 5:
            r_, g_, b_ = x, 0, c
        elif h_ >= 5 and h_ <= 6:
            r_, g_, b_ = c, 0, x
        else:
            r_, g_, b_ = 0, 0, 0

        m = v - c
        r, g, b = r_ + m, g_ + m, b_ + m

        return np.array([r * 255, g * 255, b * 255])


    def make_restaurant_dict(self, weight):
        dict = {
            'weight': str(weight),
        }
        return dict

    def make_restroom_dict(self, rgb, size):
        dict = {
            'RGB': str(rgb),
            'size': str(size)  # 소수점 세번째까지
        }
        return dict

    def restroom(self, img):
        # adjusting brightness
        bright = 200 - np.mean(img)
        img = np.clip(img + bright, 0, 255).astype(np.uint8)
        # plt.imshow(img)
        # plt.show()

        # segmentation
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        flat_image = np.reshape(img, [-1, 3])
        kmeans = KMeans(n_clusters=self.cluster)
        kmeans.fit(flat_image)
        labels = kmeans.labels_
        labels = np.reshape(labels, img.shape[:2])
        # plt.imshow(labels)
        # plt.show()

        # size, color
        numlabels = np.arange(0, len(np.unique(labels)) + 1)
        (hist, _) = np.histogram(labels, bins=numlabels)
        hist = hist.astype('float')
        sizes = hist / hist.sum()
        hsvs = kmeans.cluster_centers_
        # print('sizes    :', sizes)

        # compare color
        result_list = []
        for i in range(len(hsvs)):
            rgb = self.hsv2rgb(hsvs[i])
            if rgb[0] < 180 or rgb[1] < 180 or rgb[2] < 180:
                result_list.append((hsvs[i], sizes[i]))
                # print('hsv      :', hsvs[i])
                # print('rgb      :', rgb)
                # plt.imshow(cv2.cvtColor(np.tile(hsvs[i], (100, 100, 1)).astype('uint8'), cv2.COLOR_HSV2RGB))
                # plt.show()

        small_rgb = None
        big_rgb = None
        white = np.array([255, 255, 255])
        for i in range(len(result_list)):
            color, size = result_list[i]
            rgb = self.hsv2rgb(color).astype('uint8')

            if color[2] < 150:
                if big_rgb is None or np.linalg.norm(big_rgb - white) < np.linalg.norm(rgb - white):
                    big_rgb = rgb
                    rgb = '#' + str(hex(rgb[0]))[2:] + str(hex(rgb[1]))[2:] + str(hex(rgb[2]))[2:]
                    dict = self.make_restroom_dict(rgb, round(size * 100, 3))
                    print('poo  :', dict)
                    self.send_json(dict, 'poo')
            else:
                if small_rgb is None or np.linalg.norm(small_rgb - white) < np.linalg.norm(rgb - white):
                    rgb = '#' + str(hex(rgb[0]))[2:] + str(hex(rgb[1]))[2:] + str(hex(rgb[2]))[2:]
                    dict = self.make_restroom_dict(rgb, round(size * 100, 3))
                    print('pee  :', dict)
                    self.send_json(dict, 'pee')

    def restaurant(self, weight_list):
        weights = np.array(weight_list)

        quantile = np.percentile(weights, [25, 75], interpolation='nearest')
        iqr = quantile[1] - quantile[0]
        outlier_max = iqr * 1.5 + quantile[1]
        result = weights[np.where(weights <= outlier_max)]
        dict = self.make_restaurant_dict(result.max() - result.min())
        print(dict)
        self.send_json(dict, 'intake')

    def send_json(self, data, where):
        URL = 'http://13.209.18.94:3000/info/' + where

        res = requests.post(URL, json=data, headers = {'Authorization':self.uid})
        #print('POST    :', res.status_code)
        #print(res.text)
        return res
