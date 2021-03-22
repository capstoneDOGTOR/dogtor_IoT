import threading    
import bluepy.btle
from bluepy.btle import *
target_name = "ELA_106"   # target device name
target_address = None     # target device address
weight_service_uuid = "ef680400-9b35-4933-9b10-52ffa9740042"
camera_service_uuid = "ef680406-9b35-4933-9b10-52ffa9740042"
count = 0
data_flag = 0
threads = []
Peripherals = []


def findDevice (self) : 
        target_name = "ELA_106"   # target device name
        target_address = None     # target device address
        scanner = Scanner()
        devices = scanner.scan(3.0)
        for dev in devices:
            print (dev)
            for (_, _, value) in dev.getScanData():
                if target_name == value: 
                    target_address = dev.addr
                    # create peripheral class
                    peripheral = Peripheral(target_address, "random")
                    print("I Find Device")
                    return peripheral
        return 

class MyDelegate(DefaultDelegate):                    #Constructor (run once on startup)
    def __init__(self, params):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):      #func is caled on notifications
        motion_data = struct.unpack('hhhhhhhhh',data) # 18byte
    


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)



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

    #     print (Peripherals[iter].addr + " : Notification is turned on for Raw_data")
    #     t = threading.Thread(target = RCV_IMU, args = (Peripherals[iter],iter, len(Peripherals)))
    #     threads.append(t)


    # for iter in range(len(threads)) :
    #     threads[iter].start()

    # for iter in range(len(threads)) :
    #     threads[iter].join()


if __name__ == '__main__':
    main()
