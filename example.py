from bluepy.btle import *
import threading    
import bluepy.btle
# from data_process import *
    

def findDevice () : 
    target_name = "BT04"   # target device name
    target_address = None     # target device address
    scanner = Scanner()
    devices = scanner.scan(3.0)
    for dev in devices:     # motion_data = struct.unpack('hhhhhhhhh',data) # 18byte
        for (_, _, value) in dev.getScanData():
            if target_name in value: 
                target_address = dev.addr
                # create peripheral class
                peripheral = Peripheral(target_address, "public")
                print("I Find Device")
                return peripheral
    return 

class MyDelegate(DefaultDelegate):                    #Constructor (run once on startup)
    def __init__(self, params):
        DefaultDelegate.__init__(self)
        self.time = time.time()
        self.weightList = []

    def handleNotification(self, cHandle, data):      #func is caled on notifications
        print(data.decode('utf-8'))
        currentTime = time.time()
        self.weightList.append(data.decode ('utf-8'))
        if ( self.time - currentTime > 20) :
            self.time = currentTime 
            Parce = Parcing()
            Cam = Camera()
            print('color...')
            img = Cam.capture()
            color = Parce.restroom(img)
            data_send = make_dict(name1 = 'color', val1 = color, name2='eat', val2=food)
            response = Parce.send_json(data_send)
            print('response :', response.status_code)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)


def rcv_data (device) :
    chList = device.getCharacteristics()
    # print ("Handle   UUID                                Properties")
    # print ("-------------------------------------------------------")                 
    # for ch in chList:
    #     print ("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.uuid) +" " + ch.propertiesToString())
    device.writeCharacteristic(36, struct.pack('<bb', 0x01, 0x00), withResponse=True)

    while (True):    
        if device.waitForNotifications(1.0) :
            pass
        else :
            pass
        

def main():
    #bluepy.btle.Debugging = True
    print("main")
    peripheral = findDevice()
    if peripheral :
        pass
    else :
        print ("The device cannot be found")
        return 
    delegate = MyDelegate(peripheral)
    peripheral.setDelegate(delegate)
    print(peripheral.addr," : Notification is turned on for Raw_data")
    rcv_data(peripheral)


    # for iter in range(len(Peripherals)) :
    #     Peripherals[iter].setDelegate(MyDelegate(Peripherals[iter]) )
    #     # Get MotionService
    #     MotionService=Peripherals[iter].getServiceByUUID(motion_service_uuid)
    #     # Get The Motion-Characteristics
    #     MotionC = MotionService.getCharacteristics(motion_char_uuid)[0]
    #     # Get The handle tf the  Button-Characteristics
    #     hMotionC = MotionC.getHandle()+1
    #     # Turn notifications on by setting bit0 in the CCC more info on:
    #     Peripherals[iter].writeCharacteristic(hMotionC, struct.pack('<bb', 0x01, 0x00), withResponse=True)

    print (Peripherals[iter].addr + " : Notification is turned on for Raw_data")
    t = threading.Thread(target = RCV_IMU, args = (Peripherals[iter],iter, len(Peripherals)))
    threads.append(t)


    # for iter in range(len(threads)) :
    #     threads[iter].start()

    # for iter in range(len(threads)) :
    #     threads[iter].join()

if __name__ == '__main__':
    main()