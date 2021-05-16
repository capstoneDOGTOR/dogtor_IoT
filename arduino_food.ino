#include "HX711.h"
#include <SoftwareSerial.h>

// DOUT = A1
// SCK = A0
// RX = 7
// TX = 8
// button = 2
HX711 scale1(A0, A1);
SoftwareSerial mySerial(8, 7);
int button = 2;

flag = 0
weight = 0
unsigned long start_time = 0;
unsigned long now_time = 0;
int eating_time = 10000;

void setup() {
  scale1.set_scale(-405.0);    // this value is obtained by calibrating the scale with known weights; see the README for details
  scale1.tare();
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(button, INPUT_PULLUP);
  attachInterrupt(0, buttoninterrupt, FALLING);
}

void loop() {

    if (flag == 1) {
      before_weight = scale1.get_units(5);
      now_weight = scale1.get_units(5);
      if (before_weight != now_weight) {
        start_time = (unsigned long)millis();
        flag = 2;
      }
      else {
        delay(3000);
      }
    }

    if (flag == 2) {
        Serial.println("max/" + String(weight));
        mySerial.print("max/" + String(weight));
        flag = 3;
    }

    if (flag == 3) {
        now_time = (unsigned long)millis();
        weight = scale1.get_units(5);
        if (now_time - start_time < eating_time) {
          Serial.println("data/" + String(weight));
          mySerial.print("data/" + String(weight));
        }
        else {
          max_weight = weight;
          Serial.println("end");
          mySerial.print("end");
          flag = 1;
        }
        delay(1000);
    }
}

void buttoninterrupt() {
  max_weight = scale1.get_units(5);
  flag = 1;
}
