from send import *
from process_img import *

class Parcing():
    def __init__(self, uid):
        self.cluster = 5
        self.send = send(uid)

    def restroom(self, img, weight):

        poo, pee = process_img(img, self.cluster)

        #send to server
        if poo['size'] != 0 or pee['size'] != 0:
            dict = self.make_weight_dict(weight)
            print(dict)
            # self.send.send_json(dict, 'weight')

        if poo['size'] != 0:
            rgb = poo['rgb'].astype('uint8')
            hsv = poo['hsv'].astype('uint8')
            size = round(poo['size']* 100, 3)
            color = hsv2color(hsv, rgb)
            if color == 'brown':
                flag = True
            else:
                flag = False

            send_rgb = '#' + str(hex(rgb[0]))[2:] + str(hex(rgb[1]))[2:] + str(hex(rgb[2]))[2:]
            send_hsv = str(hsv[0]) + '/' + str(hsv[1]) + '/'+ str(hsv[2])

            dict = self.make_restroom_dict(send_rgb, send_hsv , size, color, flag)
            print('poo  :', dict)
            self.send.send_json(dict, 'poo')

        if pee['size'] != 0:
            rgb = pee['rgb'].astype('uint8')
            hsv = pee['hsv'].astype('uint8')
            size = round(pee['size']* 100, 3)
            color = hsv2color(hsv, rgb)
            if color == 'yellow':
                flag = True
            else:
                flag = False

            send_rgb = '#' + str(hex(rgb[0]))[2:] + str(hex(rgb[1]))[2:] + str(hex(rgb[2]))[2:]
            send_hsv = str(hsv[0]) + '/' + str(hsv[1]) + '/' + str(hsv[2])

            dict = self.make_restroom_dict(send_rgb, send_hsv , size, color, flag)
            print('pee  :', dict)
            self.send.send_json(dict, 'pee')


    def restaurant(self, weight_list):
        weights = np.array(weight_list, dtype = np.int64)
        print("weights List ", weights)
        max = weights[0]
        quantile = np.percentile(weights, [25, 75], interpolation='nearest')
        iqr = (quantile[1]) - (quantile[0])
        outlier_max = iqr * 1.5 + (quantile[1])
        result = weights[np.where(weights <= outlier_max)]
        result = result[np.where(weights > 0)]
        
        dict = self.make_restaurant_dict(max- result.min())
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

    def make_restroom_dict(self, rgb, hsv, size, color, flag):
        dict = {
            'RGB': str(rgb),
            'HSV': str(hsv),
            'size': str(size),  # 소수점 세번째까지
            'color': color,
            'flag': flag
        }
        return dict
