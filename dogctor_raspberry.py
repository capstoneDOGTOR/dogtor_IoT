from bluepy.btle import *
import threading    
import bluepy.btle
# from data_process import *

def findDevice () : 
    target_name = "BT04"   # target device name
    target_address = None     # target device address
    scanner = Scanner()
    devices = scanner.scan(3.0)
    for dev in devices:    
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
        self.currentTime = 0
        self.weightList = []


    def handleNotification(self, cHandle, data):      #func is caled on notifications
        print(data.decode('utf-8'))
        self.currentTime = time.time()
        self.weightList.append(data.decode ('utf-8'))
        if ( self.time - self.currentTime > 20) :
            self.upload()

    def upload (self) :
        self.time = self.currentTime 
        Parce = Parcing()
        Cam = Camera()
        print('color...')
        img = Cam.capture()
        color = Parce.restroom(img)
        food = Parce.restaurant(self.weightList)
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


def rcv_data (device,  delegate) :
    timelimit = 20
    last = -1
    chList = device.getCharacteristics()
    print ("Handle   UUID                                Properties")
    print ("-------------------------------------------------------")                 
    for ch in chList:
        print ("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.uuid) +" " + ch.propertiesToString())
    device.writeCharacteristic(36, struct.pack('<bb', 0x01, 0x00), withResponse=True)
    while (True):    
        if device.waitForNotifications(1.0) :
            last = time.time()
            pass
        else :
            if (last - time.time() > 60):
                delegate.upload()
            else :
                pass

def main():
    threads = []
    #bluepy.btle.Debugging = True
    print("main")
    while (True):
        while (True) :
            peripheral = findDevice()
            if peripheral :
                break
            else :
                print ("The device cannot be found")
                # time.sleep(10)
        delegate = MyDelegate(peripheral)
        peripheral.setDelegate(delegate)
        print("Find Device")

        t = threading.Thread(target = rcv_data, args =  (peripheral,delegate ))
        threads.append(t)

        for iter in range(len(threads)) :
            threads[iter].start()

        for iter in range(len(threads)) :
            threads[iter].join()

        # rcv_data(peripheral,delegate )

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

        # print (Peripherals[iter].addr + " : Notification is turned on for Raw_data")
  

if __name__ == '__main__':
    main()