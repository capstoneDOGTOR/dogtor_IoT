# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

import bluetooth
from bluetooth import *
# def receiveMessages():
#   server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
#   port = 1
#   server_sock.bind(("",port))
#   server_sock.listen(1)
  
#   client_sock,address = server_sock.accept()
#   print ("Accepted connection from " + str(address))
  
#   data = client_sock.recv(1024)
#   print ("received [%s]" % data)
  
#   client_sock.close()
#   server_sock.close()
  
# def sendMessageTo(targetBluetoothMacAddress):
#   port = 1
#   sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#   sock.connect((targetBluetoothMacAddress, port))
#   sock.send("hello!!")
#   sock.close()
  
# def lookUpNearbyBluetoothDevices():
#   nearby_devices = bluetooth.discover_devices()
#   for bdaddr in nearby_devices:
#     print (str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
    
    
# lookUpNearbyBluetoothDevices()


def receiveMsg():
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    # RFCOMM 포트를 통해 데이터 통신을 하기 위한 준비    
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(('',PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    # 블루투스 서비스를 Advertise
    advertise_service( server_sock, "BtChat",
            service_id = uuid,
            service_classes = [ uuid, SERIAL_PORT_CLASS ],
            profiles = [ SERIAL_PORT_PROFILE ] )
    
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
            print("received [%s]" % data)
            print("send [%s]" % data[::-1])
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

receiveMsg()