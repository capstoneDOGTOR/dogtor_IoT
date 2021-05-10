def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")

def weight():
    EMULATE_HX711 = False

    if not EMULATE_HX711:
        import RPi.GPIO as GPIO
        from hx711py.hx711 import HX711
    else:
        from hx711py.emulated_hx711 import HX711

    hx1 = HX711(16, 20)
    hx2 = HX711(19, 26)
    referenceUnit = 1

    hx1.set_reading_format("MSB", "MSB")
    hx2.set_reading_format("MSB", "MSB")
    hx1.set_reference_unit(referenceUnit)
    hx2.set_reference_unit(referenceUnit)
    hx1.reset()
    hx2.reset()
    hx1.tare()
    hx2.tare()
    print("Tare done! Add weight now...")

    val1 = hx1.get_weight(5)
    val2 = hx2.get_weight(5)
    return val1 + val2
