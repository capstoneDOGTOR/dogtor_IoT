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
int flag = 1;
unsigned long start_time = 0;
unsigned long now_time = 0;
int before_weight = 0;
int now_weight = 0;

void setup() {
  scale1.set_scale(-405.0);    // this value is obtained by calibrating the scale with known weights; see the README for details
  scale1.tare();
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(button, INPUT_PULLUP);
}
void loop() {
  if (digitalRead(button) == LOW) {
    now_weight = scale1.get_units(5);
    Serial.println("max" + String(weight));
    mySerial.print("max" +String(weight));
  }

  now_weight = scale1.get_units(5);
  if (now_weight != before_weight) {
    start_time = (unsigned long)millis();
    flag = 2;
  }

  if (flag == 2) {
    now_time = (unsigned long)millis();

    while (1) {
      if (now_time - start_time == 600000) {
        flag = 1;
        Serial.println("end");
        mySerial.print("end");
        break;
    }
      else {
        weight = scale1.get_units(5);
        Serial.println(weight);
        mySerial.print(weight);
      }
    delay(1000);
    }
  }

}