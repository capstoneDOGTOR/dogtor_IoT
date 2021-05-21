#include "HX711.h"
#include <SoftwareSerial.h>

// DOUT = A1
// SCK = A0
// RX = 7
// TX = 8
// button = 2
HX711 scale1(A0, A1);
SoftwareSerial mySerial(8, 7);
int button = 2; // interrupt pin

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
  attachInterrupt(0, buttoninterrupt, FALLING); // interrupt num, funcion name, mode:Falling(HIGH->LOW)
}

void loop() {

    if (flag == 1) { // wait
      before_weight = scale1.get_units(5);
      delay(3000);
      now_weight = wscale1.get_units(5);

      if (before_weight != now_weight) { // dog does touch his/her food
        if (now_weight > 0) {
          start_time = (unsigned long)millis();
          flag = 2;
        }
      }
      else {                            // dog does not touch his/her food
        delay(3000);
      }
    }

    if (flag == 2) { // start
        Serial.println("max/" + String(max_weight));
        mySerial.print("max/" + String(max_weight));
        flag = 3;
    }

    if (flag == 3) { // send
        now_time = (unsigned long)millis();
        weight = scale1.get_units(5);
        if (now_time - start_time < eating_time) { // eating for eating_time
          Serial.println("data/" + String(weight));
          mySerial.print("data/" + String(weight));
        }
        else {                                     // stop eating
          max_weight = weight;
          Serial.println("end");
          mySerial.print("end");
          flag = 1;
        }
        delay(1000); // once for 10 seconds.
    }
}

void buttoninterrupt() { // interrupt, user push the button
    // use debounce if it doesnt't work well
    max_weight = scale1.get_units(5);
    flag = 1;
}