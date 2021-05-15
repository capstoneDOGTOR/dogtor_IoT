from bluepy.btle import *
import threading    
import bluepy.btle
from data_process import *


def setWifi():
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    uid =""
    wifi_name = ""
    wifi_password = ""
 

    # RFCOMM 포트를 통해 데이터 통신을 하기 위한 준비    
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(('',PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    # # 블루투스 서비스를 Advertise
    # advertise_service( server_sock, "setWifi",
    #         service_id = uuid,
    #         service_classes = [ uuid, SERIAL_PORT_CLASS ],
    #         profiles = [ SERIAL_PORT_PROFILE ] )
    
    print("Waiting for connection : channel %d" % port)
    # 클라이언트가 연결될 때까지 대기
    client_sock, client_info = server_sock.accept()
    print('accepted')
    while True:          
        print("Accepted connection from ", client_info)
        try:
            # 들어온 데이터를 역순으로 뒤집어 전달
            data = client_sock.recv(1024)
            if len(data) == 0: break
            if "from_app" in data:
                array  =  data.split('/')
                uid = array[1]
                wifi_name = array[2]
                wifi_password = array[3]
                os.system('sed \'/}$/a\\network={\\n        ssid=\"'+wifi_name+'\"\\n        psk=\"'+wifi_password+'\"\\n        key_mgmt=WPA-PSK\\n        disabled=1\\n}\' /etc/wpa_supplicant/wpa_supplicant.conf')
                os.system('reboot')
            print("uid          :" +uid)
            print("wifi_name    :"+wifi_name)
            print("wifi_password:"+wifi_password)


            client_sock.send(data[::-1])
        except IOError:
            print("disconnected")
            client_sock.close()
            server_sock.close()
            print("all done")
            break

        except KeyboardInterrupt:
            print("disconnected")
            client_sock.close()
            server_sock.close()
            print("all done")
            break




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
                return peripheral
    return 

class MyDelegate(DefaultDelegate):            
    #Constructor (run once on startup)
    def __init__(self, params):
        DefaultDelegate.__init__(self)
        self.time = time.time()
        self.currentTime = 0
        self.weightList = []
        self.parce = Parcing()
        self.cam = Camera()
     #func is called on notifications
    def handleNotification(self, cHandle, data):     
        print("Get Data :" ,data.decode('utf-8'), "g")
        self.currentTime = time.time()
        self.weightList.append(int(data.decode ('utf-8')))
        if (self.currentTime - self.time > 20) :
            self.upload()

    def upload (self) :
        print("Data Analysis...")
        try :
            self.time = self.currentTime 
            img = self.cam.capture()
            color = self.parce.restroom(img)
            food = self.parce.restaurant(self.weightList)
            self.weightList = []
            print("Data Analysis Done")
            data_send = make_dict(name1 = 'color', val1 = color, name2='eat', val2=food)
            response = self.parce.send_json(data_send)
            print('response :', response.text)
        except :
            pass

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
    weight_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
    chList = device.getCharacteristics()
    print ("Handle   UUID                                Properties")
    print ("-------------------------------------------------------")                 
    for ch in chList:
        if ch.uuid == weight_UUID :
            weightHandle = ch.getHandle()+1
        print ("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.uuid) +" " + ch.propertiesToString())
    # Turn notifications on weight Service 
    device.writeCharacteristic(weightHandle, struct.pack('<bb', 0x01, 0x00), withResponse=True)
    
    
    while (True):    
        if device.waitForNotifications(1.0) :
            last = time.time()
            pass
        else :
            if (time.time() - last   > 60):
                delegate.upload()
            else :
                pass

def main():
    threads = []
    #bluepy.btle.Debugging = True
    while (True):
        while (True) :
            peripheral = findDevice()
            if peripheral :
                break
            else :
                print ("The device cannot be found")
                # time.sleep(10)

        #set Delegate into peripheral object
        delegate = MyDelegate(peripheral)
        peripheral.setDelegate(delegate)
        print("Find Device")
        t = threading.Thread(target = rcv_data, args =  (peripheral,delegate ))
        threads.append(t)
        t = threading.Thread(target = setWifi)
        threads.append(t)
        for iter in range(len(threads)) :
            threads[iter].start()
        for iter in range(len(threads)) :
            threads[iter].join()


if __name__ == '__main__':
    main()
