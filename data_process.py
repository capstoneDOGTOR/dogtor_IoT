import numpy as np
import cv2
# import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import statistics

from send import *

class Parcing():
    def __init__(self, uid):
        self.cluster = 5
        self.send = send(uid)

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

        return np.array([r * 255, g * 255, b * 255]).astype('uint8')

    def find_pad(self, img):
        mark = np.copy(img)

        b_threshold = 200
        g_threshold = 200
        r_threshold = 200

        thresholds = (img[:, :, 0] > b_threshold) & (img[:, :, 1] > g_threshold) & (img[:, :, 2] > r_threshold)
        mark[thresholds] = [255, 255, 255]

        # plt.imshow(cv2.cvtColor(mark, cv2.COLOR_BGR2RGB))
        # plt.show()
        return mark

    def region_of_interest(self, img, vertices):
        mask = np.zeros_like(img)
        color = (255, 255, 255)

        cv2.fillPoly(mask, vertices, color)
        # plt.imshow(mask)
        # plt.show()

        roi_image = cv2.bitwise_and(img, mask)
        # plt.imshow(cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB))
        # plt.show()

        return roi_image

    def restroom(self, img, weight):
        # brightness
        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # plt.show()
        # bright = 220 - np.mean(img)
        # img = np.clip(img + bright, 0, 255).astype(np.uint8)
        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # plt.show()

        # ROI, preprocessing
        vertices = np.array([[(0, 360), (60, 312), (529, 292), (640, 364), (640, 480), (0, 480)]], dtype=np.int32)  # 수정

        roi_img = self.region_of_interest(img, vertices)  # vertices에 정한 점들 기준으로 ROI 이미지 생성
        cv2.imwrite('./sample2.jpg', roi_img)
        img = self.find_pad(roi_img)

        # segmentation
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        flat_image = np.reshape(img, [-1, 3])
        kmeans = KMeans(n_clusters=self.cluster)
        kmeans.fit(flat_image)
        labels = kmeans.labels_
        labels = np.reshape(labels, img.shape[:2])
        # plt.imshow(labels)
        # plt.show()
        # cv2.imwrite('./sample3.jpg', labels)

        # size, color
        numlabels = np.arange(0, len(np.unique(labels)) + 1)
        (hist, _) = np.histogram(labels, bins=numlabels)
        hist = hist.astype('float')
        sizes = hist / hist.sum()
        colors = np.array([[int(x[0]),int(x[1]),int(x[2])] for x in kmeans.cluster_centers_])

        # print('color    :', colors)
        # print('sizes    :', sizes)

        black = np.array([0,0,0])
        white = np.array([200,200,200])

        poo_rgb = np.array([0,0,0])
        poo_hsv = np.array([0,0,0])
        poo_size = 0
        poo_cnt = 0
        pee_rgb = np.array([0,0,0])
        pee_hsv = np.array([0,0,0])
        pee_size = 0
        pee_cnt = 0
        for i in range(len(colors)):
            rgb = self.hsv2rgb(colors[i])
            hsv = colors[i]
            size = round(sizes[i] * 100, 3)
            # print('hsv      :', hsv)
            # print('rgb      :', rgb)
            # print('size     :', size)
            # plt.imshow(np.tile(rgb, (100, 100, 1)) / 255)
            # plt.show()

            if (rgb == black).all() or (rgb > white).all():
                # print('a')
                continue

            if hsv[2] < 150:
                # print('b')
                poo_rgb += rgb
                poo_hsv += hsv
                poo_size += size
                poo_cnt += 1
            else:
                # print('c')
                pee_rgb += rgb
                pee_hsv += hsv
                pee_size += size
                pee_cnt += 1

        if poo_cnt + pee_cnt != 0:
            dict = self.make_weight_dict(weight)
            print(dict)
            self.send.send_json(dict, 'weight')

        if poo_cnt != 0:
            poo_rgb = (poo_rgb/poo_cnt).astype('uint8')
            poo_hsv = (poo_hsv/poo_cnt).astype('uint8')
            poo_color = self.hsv2color(poo_hsv)

            poo_rgb = '#' + str(hex(poo_rgb[0]))[2:] + str(hex(poo_rgb[1]))[2:] + str(hex(poo_rgb[2]))[2:]
            poo_hsv = str(poo_hsv[0]) + '/' + str(poo_hsv[1]) + str(poo_hsv[2])
            dict = self.make_restroom_dict(poo_rgb, poo_hsv, round(poo_size,3), poo_color)
            print('poo  :', dict)
            self.send.send_json(dict, 'poo')

        if pee_cnt != 0:
            pee_rgb = (pee_rgb / pee_cnt).astype('uint8')
            pee_hsv = (pee_hsv / pee_cnt).astype('uint8')
            pee_color = self.hsv2color(pee_hsv)

            pee_rgb = '#' + str(hex(pee_rgb[0]))[2:] + str(hex(pee_rgb[1]))[2:] + str(hex(pee_rgb[2]))[2:]
            pee_hsv = str(pee_hsv[0]) + '/' + str(pee_hsv[1]) + str(pee_hsv[2])
            dict = self.make_restroom_dict(pee_rgb, pee_hsv, round(pee_size,3), pee_color)
            print('pee  :', dict)
            self.send.send_json(dict, 'pee')

    def restaurant(self, weight_list):
        weights = np.array(weight_list)

        quantile = np.percentile(weights, [25, 75], interpolation='nearest')
        iqr = quantile[1] - quantile[0]
        outlier_max = iqr * 1.5 + quantile[1]
        result = weights[np.where(weights <= outlier_max)]
        dict = self.make_restaurant_dict(result.max() - result.min())
        print(dict)
        self.send.send_json(dict, 'intake')

    def hsv2color(self, hsv):
        h = hsv[0] * 2
        s = int(hsv[1] / 255)
        v = int(hsv[2] / 255)

        if v < 15:
            if s < 10:
                return 'gray'
            return 'black'

        if (h >= 0 and h < 20) or (h >= 340):
            if s >= 20 and s < 70:
                return 'pink'
            else:
                return 'red'
        elif h >= 20 and h < 40:
            if s + v > 150:
                return 'orange'
            else:
                return 'brown'
        elif h >= 40 and h < 70:
            return 'yellow'
        elif h >= 70 and h < 170:
            return 'green'
        elif h >= 170 and h < 340:
            return 'purple'

    def make_weight_dict(self, weight):
        dict = {
            'weight': str(round(weight, 0)),
        }
        return dict

    def make_restaurant_dict(self, weight):
        dict = {
            'amountOfMeal': str(weight)
        }
        return dict

    def make_restroom_dict(self, rgb, hsv, size, color):
        dict = {
            'RGB': str(rgb),
            'HSV': str(hsv),
            'size': str(size),  # 소수점 세번째까지
            'color': color
        }
        return dict
