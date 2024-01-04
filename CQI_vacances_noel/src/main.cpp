#include "ESP8266WiFi.h"
#include "ESPAsyncWebServer.h"
#include <Arduino.h>
#include <Servo.h>

#define servoPin_pince D0
#define servoPin_updown D1
#define servoPin_flip D2

#define motor1Pin1 D3
#define motor1Pin2 D4
#define motor2Pin1 D5
#define motor2Pin2 D6

// instances de servos
Servo servo_pince;
Servo servo_updown;
Servo servo_flip;

const char *ssid = "Je suis Dieu et dispo";
const char *password = "123456789";

void setup_esp_wifi(const char *ssid, const char *password);

void requestHandler(AsyncWebServerRequest *request);

void initialize_servos(void);
void command_servos(int16_t angle_pince, int16_t angle_updown, int16_t angle_flip);

void initialize_motors(void);
void command_speed(int8_t speed, float correction);
void null_speed(void);

void forward(uint8_t speed, float correction);
void backward(uint8_t speed, float correction);

void rotate_clock(void);
void rotate_counter_clock(void);

AsyncWebServer server(80);
 
void setup()

{ 
  // init servo
  initialize_servos();
  analogWriteFreq(50);
  // init motors
  initialize_motors();

  Serial.begin(115200);

  Serial.println("Starting");
 
  setup_esp_wifi(ssid, password);

  server.on("/patate", HTTP_GET, [](AsyncWebServerRequest *request){
      requestHandler(request);
    });
  
  server.begin();

}
 
void loop(){
}

void forward(uint8_t speed, float correction)
{
  speed = (uint8_t)map(speed, 0, 100, 0, 255);
  Serial.println(speed);

  analogWrite(motor1Pin1, speed);
  analogWrite(motor1Pin2, 0);

  // Ajouter la correction par après
  analogWrite(motor2Pin1, speed * correction);
  analogWrite(motor2Pin2, 0);
}

void backward(uint8_t speed, float correction)
{
  speed = (uint8_t)map(speed, 0, 100, 0, 255);
  map(speed, 0, 255, 0, 100);

  analogWrite(motor1Pin1, 0);
  analogWrite(motor1Pin2, speed);

  // Ajouter la correction par après
  analogWrite(motor2Pin1, 0);
  analogWrite(motor2Pin2, speed * correction);
}

void requestHandler(AsyncWebServerRequest *request){

  Serial.println("requestHandler");

  uint16_t key = (uint16_t)(request->getParam("key")->value().toInt());

  Serial.print("angle_pince : ");
  Serial.println(key);
  
  /* int16_t angle_pince = (int16_t)(request->getParam("pince")->value().toInt());
  int16_t angle_updown = (int16_t)(request->getParam("up_down")->value().toInt());
  int16_t angle_flip = (int16_t)(request->getParam("flip")->value().toInt()); */

/*   int8_t speed = (int8_t)(request->getParam("speed")->value().toInt());
  float correction = (float)(request->getParam("correction")->value().toFloat());

  bool right = (bool)(request->getParam("right")->value().toInt());
  bool left = (bool)(request->getParam("left")->value().toInt()); */



/* 
  Serial.print("pince : ");
  Serial.print(angle_pince);
  Serial.print(" updown : ");
  Serial.print(angle_updown);
  Serial.print(" flip : ");
  Serial.println(angle_flip); 
 

  command_servos(angle_pince, angle_updown, angle_flip);

 
  Serial.print(" speed : ");
  Serial.print(speed);
  Serial.print(" correction : ");
  Serial.print(correction);
 
  command_speed(speed, correction);

  Serial.print(" right : ");
  Serial.print(right);
  Serial.print(" left : ");
  Serial.println(left);

  if (right){
    rotate_clock();
  }
  else if (left){
    rotate_counter_clock();
  }  */

}


void initialize_servos(void)
{
  servo_pince.attach(servoPin_pince, 620, 2420);
  servo_updown.attach(servoPin_updown, 620, 2420);
  servo_flip.attach(servoPin_flip, 620, 2420);

  servo_pince.write(0);
  servo_updown.write(0);
  servo_flip.write(0);

}

void command_servos(int16_t angle_pince, int16_t angle_updown, int16_t angle_flip)
{
  
  servo_pince.write(angle_pince);
  servo_updown.write(angle_updown);
  servo_flip.write(angle_flip);
}

void initialize_motors(void){
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);

  analogWrite(motor1Pin1, 0);
  analogWrite(motor1Pin2, 0);
  analogWrite(motor2Pin1, 0);
  analogWrite(motor2Pin2, 0);
}

void null_speed(void){
  analogWrite(motor1Pin1, 0);
  analogWrite(motor1Pin2, 0);
  analogWrite(motor2Pin1, 0);
  analogWrite(motor2Pin2, 0);
}

void command_speed(int8_t speed, float correction){
  if (speed > -20 and speed < 20){
    null_speed();
    return;
  }
  else if (speed > 20){
    forward(speed, correction);
  }
  else if (speed < 20){
    backward(-speed, correction);
  }
}

void rotate_counter_clock(void){
  analogWrite(motor1Pin1, 0);
  analogWrite(motor1Pin2, 255);
  analogWrite(motor2Pin1, 255);
  analogWrite(motor2Pin2, 0);

  delay(200);

  null_speed();

}

void rotate_clock(void){
  analogWrite(motor1Pin1, 255);
  analogWrite(motor1Pin2, 0);
  analogWrite(motor2Pin1, 0);
  analogWrite(motor2Pin2, 255);

  delay(200);

  null_speed();
}

void setup_esp_wifi(const char *ssid, const char *password){
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
}