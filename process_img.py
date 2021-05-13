import numpy as np
import cv2

def change_brightness(img):
    bright = 170 - np.mean(img)
    img = np.clip(img + bright, 0, 255).astype(np.uint8)

    return img

def find_pad(img):
    mark = np.copy(img)

    b_threshold = 200
    g_threshold = 200
    r_threshold = 200

    thresholds = (img[:, :, 0] > b_threshold) & (img[:, :, 1] > g_threshold) & (img[:, :, 2] > r_threshold)
    mark[thresholds] = [255, 255, 255]

    # plt.imshow(cv2.cvtColor(mark, cv2.COLOR_BGR2RGB))
    # plt.show()
    return mark


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    color = (255, 255, 255)

    cv2.fillPoly(mask, vertices, color)
    roi_image = cv2.bitwise_and(img, mask)

    return roi_image


def find_edge(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 흑백이미지로 변환
    blur_img = cv2.GaussianBlur(gray_img, (3, 3), 0)  # Blur 효과
    canny_img = cv2.Canny(blur_img, 70, 210)  # Canny edge 알고리즘

    return canny_img


def hsv2rgb(hsv):
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

def hsv2color(hsv):
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