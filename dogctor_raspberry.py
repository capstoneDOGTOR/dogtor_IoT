from bluepy.btle import *
import threading    
import bluepy.btle
from data_process import *
import bluetooth
from bluetooth import *
import subprocess
import os
from iot import *
from send import *

<<<<<<< Updated upstream
class RCV_BT :
    def __init__(self):
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.wifi_name = ""
        self.wifi_password = ""
        self.interface = 'wlan0'
    
    def setWifi(self):
        global uid
        # RFCOMM 포트를 통해 데이터 통신을 하기 위한 준비    
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(('',PORT_ANY))
        server_sock.listen(1)
        port = server_sock.getsockname()[1]

        # 블루투스 서비스를 Advertise
        advertise_service( server_sock, "setWifi",service_id = self.uuid, service_classes = [ self.uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ] )
        
        print("Waiting for connection : channel %d" % port)
        # 클라이언트가 연결될 때까지 대기
        client_sock, client_info = server_sock.accept()
        print('accepted')
        while (True):          
            print("Accepted connection from ", client_info)
            try:
                # 들어온 데이터를 역순으로 뒤집어 전달
                data = client_sock.recv(1024)
                if len(data) == 0: 
                    if uid != "":
                        ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        try:
                            output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
                            print(output)
                            if "ESSID:\""+self.wifi_name+"\"" in output  :
                                return
                            else:
                                os.system('iwconfig ' + self.interface + ' essid ' + self.wifi_name + ' key ' + self.wifi_password)
                        except subprocess.CalledProcessError:
                            # grep did not match any lines
                            print("No wireless networks connected")
                    break
=======
def setWifi():
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    uid =""
    wifi_name = ""
    wifi_password = ""
    pin_number = 'ddddd'
 

    # RFCOMM 포트를 통해 데이터 통신을 하기 위한 준비    
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(('',PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

     # 블루투스 서비스를 Advertise
    advertise_service( server_sock, "setWifi",service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ] )
>>>>>>> Stashed changes
    
                data = data.decode()
                if "from_app" in data:
                    array  =  data.split('/')
                    uid = array[1]
                    self.wifi_name = array[2]
                    self.wifi_password = array[3]
                    # os.system('sed \'/}$/a\\network={\\n        ssid=\"'+self.wifi_name+'\"\\n        psk=\"'+self.wifi_password+'\"\\n        key_mgmt=WPA-PSK\\n        disabled=1\\n}\' /etc/wpa_supplicant/wpa_supplicant.conf')
                    # os.system('reboot')
                    print("uid          :" +uid)
                    print("self.wifi_name    :"+self.wifi_name)
                    print("self.wifi_password:"+self.wifi_password)
                    client_sock.send(data[::-1])
                    ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    try:
                        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
                        output = output.decode()
                        print(type(output))
                        if "ESSID:\""+self.wifi_name+"\"" in output  :
                            return
                        else:
                            os.system('iwconfig ' + self.interface + ' essid ' + self.wifi_name + ' key ' + self.wifi_password)
                    except subprocess.CalledProcessError:
                        # grep did not match any lines
                        print("No wireless networks connected")
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


class MyDelegate(DefaultDelegate):            
    #Constructor (run once on startup)
    def __init__(self, params):
        global uid
        DefaultDelegate.__init__(self)
        self.time = time.time()
        self.currentTime = 0
        self.weightList = []
        self.parcing = Parcing(uid)
        
     #func is called on notifications

    def handleNotification(self, cHandle, data):     
        print("Get Data :" ,data.decode('utf-8'), "g")
        data = data.decode()
        if data.startswith("max"):
            self.weightList = []
            self.weightList.append(data.split('/')[1])
        elif data.startswith("end") :
            self.parcing.restaurant(self.weightList)
        elif data.startswith("data") :
            self.weightList.append(data.split('/')[1])
        else :
            pass 
        
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

class RCV_BLE() :
    def __init__(self):
        self.target_name = "BT04"   # target device name
        self.target_address = None     # target device address
        self.uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
        pass 
    def findDevice (self) : 
        
        scanner = Scanner()
        devices = scanner.scan(3.0)
        try : 
            for dev in devices:    
                for (_, _, value) in dev.getScanData():
                    if self.target_name in value: 
                        self.target_address = dev.addr
                        # create peripheral class
                        peripheral = Peripheral(self.target_address, "public")
                        return peripheral
            return
        except bluepy.btle.BTLEDisconnectError :
            print ("Arduino disconnect")

    def rcv_data (self, device,  delegate) :
        timelimit = 20
        last = -1
        chList = device.getCharacteristics()
        print ("Handle   self.uuid                                Properties")
        print ("-------------------------------------------------------")                 
        for ch in chList:
            if ch.self.uuid == self.uuid :
                weightHandle = ch.getHandle() +1
            print ("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.self.uuid) +" " + ch.propertiesToString())
        # Turn notifications on weight Service 
        device.writeCharacteristic(weightHandle, struct.pack('<bb', 0x01, 0x00), withResponse=True)
        while (True):    
            if device.waitForNotifications(1.0) :
                pass
            else :
<<<<<<< HEAD
                print ("The device cannot be found")
                # time.sleep(10)

        #set Delegate into peripheral object
        delegate = MyDelegate(peripheral)
        peripheral.setDelegate(delegate)
        print("Find Device")
        threads.append(threading.Thread(target = rcv_data, args =  (peripheral,delegate ))) #receive data from Arduino
        threads.append(threading.Thread(target = capture, args = id))                        #capture 
        for iter in range(len(threads)) :   
            threads[iter].start()
        for iter in range(len(threads)) :
            threads[iter].join()
=======
                pass

  

class Defecation_pad :
    def __init__(self):
        pass
    def capture (self) :
        global uid
        parcing = Parcing(uid)
        weight = Weight()
        camera = Camera()
        while(True) :
            # # 2.1 무게 측정
            print('weight')
            dog_weight = weight.weight()

            # 2.2 카메라 촬영
            print('capture')

            img = camera.capture()
            # img = cv2.imread('img.JPG')
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # cv2.imwrite('./sample1.jpg', img)

            # 2.3
            print('analysis')
            parcing.restroom(img, dog_weight)


class Raspberry :
    def __init__(self):
        bluepy.btle.Debugging = True
        self.appReceiver = RCV_BT()
        self.arduinoReceiver = RCV_BLE()
        self.pad = Defecation_pad()
        self.threads = []
        
    def service (self):
        global uid
        self.appReceiver.setWifi()
        while (True):
            while (True) :
                peripheral = self.arduinoReceiver.findDevice()
                if peripheral:
                    break
                else :
                    print ("The device cannot be found")
                    # time.sleep(10)

            #set Delegate into peripheral object
            delegate = MyDelegate(peripheral)
            peripheral.setDelegate(delegate)
            print("Find Device")
            self.threads.append(threading.Thread(target = self.arduinoReceiver.rcv_data, args =  (peripheral,delegate)))    #receive data from Arduino
            self.threads.append(threading.Thread(target = self.pad.capture))                                                #capture , send to Server
            for iter in range(len(self.threads)) :   
                self.threads[iter].start()
            for iter in range(len(self.threads)) :
                self.threads[iter].join()
            self.threads = []

>>>>>>> 04604e7fb0af317dd6eeccf381b668d34c49d2d4

if __name__ == '__main__':
    rasp = Raspberry()
    rasp.service()