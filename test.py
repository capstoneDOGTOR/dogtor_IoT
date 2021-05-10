from data_process import *

uid = '123'
camera = Camera()
parcing = Parcing(uid)


# img = camera.capture()
# img = cv2.imread('img.JPG')
# img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# cv2.imwrite('./1.jpg',img)
# parcing.restroom(img)

parcing.weight()

# weight_list = [150,150,150,140,140,140,130,130,130,120,120,120,100,100,100,70,70,70,40,40,40]
# parcing.restaurant(weight_list)