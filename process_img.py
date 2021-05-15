import numpy as np
import cv2
from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt

def change_brightness(img): # 밝기 조정
    bright = 125 - np.mean(img)

    img = np.clip(img + bright, 0, 255).astype(np.uint8)

    return img

def find_pad(img): # 배변패드 위치 확인
    mark = np.copy(img)
    b_threshold = 200
    g_threshold = 200
    r_threshold = 200

    thresholds = (img[:, :, 0] > b_threshold) & (img[:, :, 1] > g_threshold) & (img[:, :, 2] > r_threshold)
    mark[thresholds] = [255, 255, 255]

    return mark


def region_of_interest(img, vertices): # ROI 설정
    mask = np.zeros_like(img)
    color = (255, 255, 255)

    cv2.fillPoly(mask, vertices, color)
    roi_image = cv2.bitwise_and(img, mask)

    return roi_image

def segmentation(img, cluster): # clustering
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    flat_image = np.reshape(img, [-1, 3])

    kmeans = KMeans(n_clusters=cluster)
    kmeans.fit(flat_image)
    labels = kmeans.labels_
    labels = np.reshape(labels, img.shape[:2])

    centers = kmeans.cluster_centers_

    return labels, centers

def size_color(labels, centers): # size, color 추출
    numlabels = np.arange(0, len(np.unique(labels)) + 1)
    (hist, _) = np.histogram(labels, bins=numlabels)
    hist = hist.astype('float')
    sizes = hist / hist.sum()
    colors = np.array([[int(x[0]), int(x[1]), int(x[2])] for x in centers])

    return sizes, colors

def masking(img, cluster): # 이미지 masking
    masks = []

    for i in range(cluster):
        mask = cv2.inRange(img, i, i)
        mask = cv2.bitwise_and(img, img, mask=mask)
        mask = mask.astype('uint8')
        ret, thresh = cv2.threshold(mask, i-1, 255, cv2.THRESH_BINARY)

        masks.append(thresh)

    return masks

def find_edge(img, cluster):
    img = np.uint8(img)

    canny_img = cv2.Canny(img, 0, cluster)

    return canny_img


def hsv2rgb(hsv):
    h = hsv[0] * 2
    s = hsv[1] / 255
    v = hsv[2] / 255

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

def hsv2color(hsv): # 색 판별
    h = hsv[0] * 2
    s = int(hsv[1] / 255 * 100)
    v = int(hsv[2] / 255 * 100)

    if s < 15:
        if v > 30:
            return 'gray'
        return 'black'

    if (h >= 0 and h < 20) or (h >= 340):
        if s < 70:
            return 'pink'
        else:
            return 'red'
    elif h >= 20 and h < 40:
        if s + v > 170:
            return 'orange'
        else:
            return 'brown'
    elif h >= 40 and h < 70:
        return 'yellow'
    elif h >= 70 and h < 170:
        return 'green'
    elif h >= 170 and h < 340:
        return 'purple'

def classify(colors, sizes, masks): # 대소변 구분
    poo = dict()
    pee = dict()
    poo['size'] = 0
    pee['size'] = 0
    black = np.array([0, 0, 0])
    white = np.array([200, 200, 200])
    kind = ['x','x','x','x','x']
    rgbs = []

    for i in range(len(colors)):
        rgb = hsv2rgb(colors[i])
        rgbs.append(rgb)
        # plt.imshow(np.tile(rgb, (100, 100, 1)) / 255)
        # plt.show()

        if (rgb == black).all():
            kind[i] = 'mask'
        elif (rgb > white).all():
            kind[i] = 'pad'
        elif colors[i][1] > 15 * 2.55:
            if colors[i][2] > 50 * 2.55:
                kind[i] = 'pee'
            else:
                kind[i] = 'poo'
        else:
            kind[i] = 'x'
        # print(kind[i])
        # print('s', colors[i][1]/255)
        # print('v', colors[i][2]/255)

    for i in range(len(colors)):
        if kind[i] == 'mask' or kind[i] == 'pad':
            continue
        size = round(sizes[i],3)

        if kind[i] == 'poo':
            if poo['size'] < size:
                poo['rgb'] = rgbs[i]
                poo['hsv'] = colors[i]
                poo['size'] = size

        if kind[i] == 'pee':
            if pee['size'] < size:
                pee['rgb'] = rgbs[i]
                pee['hsv'] = colors[i]
                pee['size'] = size

    return poo, pee

def process_img(img, cluster):
    # plt.imshow(img)
    # plt.show()

    # brightness
    # img = change_brightness(img)
    # plt.imshow(img)
    # plt.show()

    # ROI
    vertices = np.array([[(0, 360), (60, 312), (529, 292), (640, 364),
                          (640, 480), (0, 480)]], dtype=np.int32)
    img = region_of_interest(img, vertices)  # vertices에 정한 점들 기준으로 ROI 이미지 생성
    # cv2.imwrite('./sample2.jpg', img)
    # plt.imshow(img)
    # plt.show()

    # find pad
    img = find_pad(img) # image 위에서 흰색 배변패드 인식
    # cv2.imwrite('./sample3.jpg', img)
    # plt.imshow(img)
    # plt.show()

    # segmentation
    labels, centers = segmentation(img, cluster) # clustering, 색상을 기준으로 분류
    # plt.imshow(labels)
    # plt.show()

    # masking
    masks = masking(labels, cluster) # 분류된 이미지 masking
    # for img in masks:
        # plt.imshow(img)
        # plt.show()

    # find edge
    # edge = find_edge(labels, self.cluster+1)
    # cv2.imwrite('./sample4.jpg', edge)
    # plt.imshow(edge)
    # plt.show()

    # size, color
    sizes, colors = size_color(labels, centers) # 분류된 이미지의 size, color 추출
    # print('color    :', colors)
    # print('sizes    :', sizes)

    # extract color & classify
    poo, pee = classify(colors, sizes, masks) # 대소변 구분

    return poo, pee