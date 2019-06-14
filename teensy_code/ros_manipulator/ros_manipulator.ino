#if (ARDUINO >= 100)
#include <Arduino.h>
#else
#include <WProgram.h>
#endif

#include <Servo.h>
#include <ros.h>
#include <sensor_msgs/JointState.h>

ros::NodeHandle  nh;

Servo servo01;
Servo servo02;
Servo servo03;
Servo servo04;
Servo servo05;
Servo servo06;

const int ledPin = 13;

void servo_cb( const sensor_msgs::JointState& cmd_msg) {
  // set servo angle, should be from 0-180
  // value / 0.01743
  servo01.write((cmd_msg.position[0] + 1.55) / 0.01743);
  servo02.write((cmd_msg.position[1] + 0.99) / 0.01743);
  servo03.write((cmd_msg.position[2] + 1.49) / 0.01743);
  servo04.write((-1 * cmd_msg.position[3] + 1.55) / 0.01743);
  servo05.write((cmd_msg.position[4] + 2.09) / 0.01743);
  servo06.write((-1.5 * cmd_msg.position[5] + 3.14) / 0.01743);

  //Serial.println(cmd_msg.position[0] / 0.01743);

  digitalWrite(ledPin, HIGH - digitalRead(ledPin)); //toggle led
}

ros::Subscriber<sensor_msgs::JointState> sub("joint_states", servo_cb);

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(57600);
  pinMode(ledPin, OUTPUT);

  nh.initNode();
  nh.subscribe(sub);

  servo01.attach(23);
  servo02.attach(22);
  servo03.attach(21);
  servo04.attach(37);
  servo05.attach(36);
  servo06.attach(35);
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  delay(1);
}
