#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver board1 = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN  125
#define SERVOMAX  625

void setup() {
  Serial.begin(9600);
  Serial.println("Ready to receive commands!");
  board1.begin();
  board1.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');   // Read incoming command till newline
    input.trim(); // Remove any whitespace

    if (input.length() > 0) {
      int separator = input.indexOf(',');
      if (separator > 0) {
        int servo_num = input.substring(0, separator).toInt();
        int angle = input.substring(separator + 1).toInt();
        if (servo_num >= 0 && servo_num < 8 && angle >= 0 && angle <= 180) {
          int pulse = angleToPulse(angle);
          board1.setPWM(servo_num, 0, pulse);

          Serial.print("Moved servo ");
          Serial.print(servo_num);
          Serial.print(" to angle ");
          Serial.println(angle);
        } else {
          Serial.println("Invalid servo number or angle");
        }
      }
    }
  }
}

int angleToPulse(int ang) {
  int pulse = map(ang, 0, 180, SERVOMIN, SERVOMAX);
  return pulse;
}