from data_process import *
from iot import *

###################### 1. setting ################################
# 1.1 uid 받기
uid = '123'

# 1.2 IoT setting
camera = Camera()
weight = Weight()
parcing = Parcing(uid)

###################### 2. raspberry ################################
# 2.1 무게 측정
print('2.1')
val = 0
# while True:
#     val = weight.weight()
#     print(val)
#     if val > 0:
#         break

# 2.2 카메라 촬영
# print('2.2')
img = camera.capture()
# img = cv2.imread('img.JPG')
# img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
cv2.imwrite('./sample1.jpg', img)

# 2.3 parcing
print('2.3')
parcing.restroom(img, val)

###################### 3. arduino ################################
# 3.1 블루투스로 weight_list 받기
weight_list = [150,150,150,140,140,140,130,130,130,120,120,120,100,100,100,70,70,70,40,40,40]

# 3.2 parcing
parcing.restaurant(weight_list)