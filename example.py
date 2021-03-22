import bluepy

def findDevice (self) : 
        target_name = "ELA_106"   # target device name
        target_address = None     # target device address
        scanner = Scanner()
        devices = scanner.scan(3.0)
        for dev in devices:
            for (_, _, value) in dev.getScanData():
                if target_name == value:
                    target_address = dev.addr
                    # create peripheral class
                    peripheral = Peripheral(target_address, "random")
                    print("I Find Device")
                    return peripheral
        return 

