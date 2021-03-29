from data_process import *

Cam = Camera()
Parce = Parcing()

while(True):
    if True: # color
        print('color...')
        img = Cam.capture()
        color = Parce.restroom(img)
        data = make_dict(name1='color', val1=color)

    if True: # weight
        print('weight...')
        weight_list = []
        food = Parce.restaurant(weight_list)
        data = make_dict(name2='eat', val2=food)

    response = Parce.send_json(data)
    print('response :', response.status_code)