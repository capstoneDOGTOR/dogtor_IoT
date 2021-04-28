#include "HX711.h"
#include <SoftwareSerial.h>

// DOUT  - pin #A1
// PD_SCK - pin #A0
// RX = 2
// TX = 3
// button = 8
HX711 scale1(A0, A1);
SoftwareSerial mySerial(3, 2);
int button = 8;
int weight = 0;
int start = 1;

void setup() {
  scale1.set_scale(-405.0);    // this value is obtained by calibrating the scale with known weights; see the README for details
  scale1.tare();                
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(button, INPUT_PULLUP);
}
void loop() {
  if (digitalRead(button) == LOW) {
    weight = scale1.get_units(1);
    Serial.println(weight);
    mySerial.print(weight);
  }
}
