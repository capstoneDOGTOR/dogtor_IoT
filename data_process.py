import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import statistics

from send import *
from process_img import *

class Parcing():
    def __init__(self, uid):
        self.cluster = 5
        self.send = send(uid)

    def restroom(self, img, weight):
        plt.imshow(img)
        plt.show()

        # brightness
        img = change_brightness(img)
        # plt.imshow(img)
        # plt.show()

        # ROI, preprocessing
        vertices = np.array([[(0, 360), (60, 312), (529, 292), (640, 364), (640, 480), (0, 480)]], dtype=np.int32)
        img = region_of_interest(img, vertices)  # vertices에 정한 점들 기준으로 ROI 이미지 생성
        # cv2.imwrite('./sample2.jpg', img)
        # plt.imshow(img)
        # plt.show()

        #find pad
        img = find_pad(img)
        # cv2.imwrite('./sample3.jpg', img)
        # plt.imshow(img)
        # plt.show()

        #find edge
        edge = find_edge(img)
        # cv2.imwrite('./sample4.jpg', edge)
        # plt.imshow(edge)
        # plt.show()

        # segmentation
        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        flat_image = np.reshape(img, [-1, 3])
        kmeans = KMeans(n_clusters=self.cluster)
        kmeans.fit(flat_image)
        labels = kmeans.labels_
        labels = np.reshape(labels, img.shape[:2])
        plt.imshow(labels)
        plt.show()

        # size, color
        numlabels = np.arange(0, len(np.unique(labels)) + 1)
        (hist, _) = np.histogram(labels, bins=numlabels)
        hist = hist.astype('float')
        sizes = hist / hist.sum()
        colors = np.array([[int(x[0]),int(x[1]),int(x[2])] for x in kmeans.cluster_centers_])
        # print('color    :', colors)
        # print('sizes    :', sizes)

        # extract color & classify
        black = np.array([0,0,0])
        white = np.array([200,200,200])
        poo_size = 0
        poo_cnt = False
        pee_size = 0
        pee_cnt = False
        for i in range(len(colors)):
            rgb = hsv2rgb(colors[i])
            hsv = colors[i]
            size = round(sizes[i] * 100, 3)
            # print('hsv      :', hsv)
            # print('rgb      :', rgb)
            # print('size     :', size)
            # plt.imshow(np.tile(rgb, (100, 100, 1)) / 255)
            # plt.show()

            if (rgb == black).all() or (rgb > white).all():
                print('a')
                continue

            if hsv[2] < 150:
                print('b')
                if size > poo_size:
                    poo_rgb = rgb
                    poo_hsv = hsv
                    poo_size = size
                    poo_cnt = True
            else:
                print('c')
                if size > pee_size:
                    pee_rgb = rgb
                    pee_hsv = hsv
                    pee_size = size
                    pee_cnt = True

        if poo_cnt == True or pee_cnt == True:
            dict = self.make_weight_dict(weight)
            print(dict)
            self.send.send_json(dict, 'weight')

        if poo_cnt == True:
            poo_rgb = (poo_rgb/poo_cnt).astype('uint8')
            poo_hsv = (poo_hsv/poo_cnt).astype('uint8')
            poo_color = hsv2color(poo_hsv)
            poo_rgb = '#' + str(hex(poo_rgb[0]))[2:] + str(hex(poo_rgb[1]))[2:] + str(hex(poo_rgb[2]))[2:]
            poo_hsv = str(poo_hsv[0]) + '/' + str(poo_hsv[1]) + '/'+ str(poo_hsv[2])
            dict = self.make_restroom_dict(poo_rgb, poo_hsv, round(poo_size,3), poo_color)
            print('poo  :', dict)
            self.send.send_json(dict, 'poo')

        if pee_cnt == True:
            pee_rgb = (pee_rgb / pee_cnt).astype('uint8')
            pee_hsv = (pee_hsv / pee_cnt).astype('uint8')
            pee_color = self.hsv2color(pee_hsv)
            pee_rgb = '#' + str(hex(pee_rgb[0]))[2:] + str(hex(pee_rgb[1]))[2:] + str(hex(pee_rgb[2]))[2:]
            pee_hsv = str(pee_hsv[0]) + '/' + str(pee_hsv[1]) + '/' + str(pee_hsv[2])
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
