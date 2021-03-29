#include "HX711.h"
#include <SoftwareSerial.h>

// DOUT  - pin #A1
// PD_SCK - pin #A0
// RX = 2
// TX = 3
HX711 scale(A1, A0);
SoftwareSerial mySerial(3, 2);
int weight = 0;
int adc = 0; 

void setup() {
  scale.set_scale(2280.f);    // this value is obtained by calibrating the scale with known weights; see the README for details
  scale.tare();               // reset the scale to 0
  mySerial.begin(9600);
}

void loop() {
  adc = scale.get_units(10);
  if(adc <0) {
    adc = -adc;
  }
  weight = int(adc)/5*5;

  mySerial.print(weight);
  delay(500);  
}
