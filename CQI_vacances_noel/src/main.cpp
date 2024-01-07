#include "ESP8266WiFi.h"
#include "ESPAsyncWebServer.h"
#include <Arduino.h>
#include <Servo.h>

#define servoPin1 D0
#define servoPin2 D1
#define servoPin3 D2

#define motor1Pin1 D6
#define motor1Pin2 D3
#define motor2Pin1 D4
#define motor2Pin2 D5

// Mode debug : Active les prints des requêtes
#define DEBUG 0
// Mode control : Active la commande des moteurs et des servos
#define CONTROL 0
typedef struct{
  String direction = "None";
  uint16_t speed = 0;
  float correction = 0;
  uint16_t servo1 = 0;
  uint16_t servo2 = 0;
  uint16_t servo3 = 0;
  uint32_t request_count = 0;

}command_t;

uint32_t ESP_time_ref = 0;

void set_time_ref(void);

bool is_timout(uint32_t request_time);

void setup_esp_wifi(const char *ssid, const char *password);

void requestHandler(AsyncWebServerRequest *request);
void request_getParam(AsyncWebServerRequest *request, command_t *command);

void control(command_t *command);

void control_print(command_t *command);

void initialize_servos(void);
void command_servos(int16_t angle_pince, int16_t angle_updown, int16_t angle_flip);

void initialize_motors(void);
void command_speed(int8_t speed, float correction);
void null_speed(void);

void forward(uint8_t speed, float correction);
void backward(uint8_t speed, float correction);

void rotate_clock(void);
void rotate_counter_clock(void);

// instances de servos
Servo servo1;
Servo servo2;
Servo servo3;

const char *ssid = "Je suis Dieu et dispo";
const char *password = "123456789";

AsyncWebServer server(80);

command_t command;
 
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
      Serial.println("New request");
      request_getParam(request, &command);;
      
    });
  
  server.begin();

}
 
void loop(){
  if (CONTROL){
    control(&command);
  }
  else{
    null_speed();
  }
  if (DEBUG){
    control_print(&command);
  }
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

void initialize_servos(void)
{
  servo1.attach(servoPin1, 620, 2420);
  servo2.attach(servoPin2, 620, 2420);
  servo3.attach(servoPin3, 620, 2420);

  servo1.write(0);
  servo2.write(0);
  servo3.write(0);

}

void command_servos(const int16_t servo1_data, const int16_t servo2_data, const int16_t servo3_data)
{
  
  servo1.write(servo1_data);
  servo2.write(servo2_data);
  servo3.write(servo3_data);
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

void command_speed_orientation(command_t *command){
  if (command->direction == "None"){
    null_speed();
    return;
  }
  else if (command->direction == "Forward"){
    forward(command->speed, command->correction);
  }
  else if (command->direction == "Backward"){
    backward(command->speed, command->correction);
  }
  else if(command->direction == "Right"){
    rotate_clock();
  }
  else if(command->direction == "Left"){
    rotate_counter_clock();
  }
  else{
    null_speed();
  }
}

void rotate_counter_clock(void){
  analogWrite(motor1Pin1, 0);
  analogWrite(motor1Pin2, 255);
  analogWrite(motor2Pin1, 255);
  analogWrite(motor2Pin2, 0);
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

void request_getParam(AsyncWebServerRequest *request, command_t *command){
  if (request->hasParam("direction")) {
        String direction = (String)(request->getParam("direction")->value());
        command->direction = direction;

    } 

    if (request->hasParam("speed")) {
        uint16_t speed = (uint16_t)(request->getParam("speed")->value().toInt());
        command->speed = speed;

    } 

    if (request->hasParam("correction")) {
        float correction = (float)(request->getParam("correction")->value().toFloat());
        command->correction = correction;
 
    } 

     if (request->hasParam("servo1")) {
        uint16_t servo1 = (uint16_t)(request->getParam("servo1")->value().toInt());
        command->servo1 = servo1;
        
    } 

    if (request->hasParam("servo2")) {
        uint16_t servo2 = (uint16_t)(request->getParam("servo2")->value().toInt());
        command->servo2 = servo2;

    }

    if (request->hasParam("servo3")) {
        uint16_t servo3 = (uint16_t)(request->getParam("servo3")->value().toInt());
        command->servo3 = servo3;

    } 

    if (request->hasParam("request_count")) {
        uint32_t request_count = (uint32_t)(request->getParam("request_count")->value().toInt());
        command->request_count = request_count;

    }

    
}

void control(command_t *command){
  command_speed_orientation(command);
  command_servos(command->servo1, command->servo2, command->servo3);
}

void control_print(command_t *command){
  Serial.print("direction: ");
  Serial.println(command->direction);
  Serial.print("speed: ");
  Serial.println(command->speed);
  Serial.print("correction: ");
  Serial.println(command->correction);
  Serial.print("servo1: ");
  Serial.println(command->servo1);
  Serial.print("servo2: ");
  Serial.println(command->servo2);
  Serial.print("servo3: ");
  Serial.println(command->servo3);
  Serial.print("request_count: ");
  Serial.println(command->request_count);
}

void set_time_ref(void){
  ESP_time_ref = millis();
}

bool is_timout(uint32_t request_time){
  if (millis() - ESP_time_ref > (request_time + 1)){
    return true;
  }
  else{
    return false;
  }
}