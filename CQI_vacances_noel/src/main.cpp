#include <Arduino.h>
#include <Servo.h>

// Librairie cusctom CQI
#include "../lib/espControl.h"
#include "../lib/espWifi.h"

#include "ESP8266WiFi.h"
#include "ESPAsyncWebServer.h"

#define servoPin1 D0
#define servoPin2 D1
#define servoPin3 D2

#define motor1Pin1 D6
#define motor1Pin2 D3
#define motor2Pin1 D4
#define motor2Pin2 D5

// Mode debug : Active les prints des requêtes
#define DEBUG 1
// Mode control : Active la controle des moteurs et des servos
#define CONTROL 0

uint32_t ESP_time_ref = 0;

uint32_t request_counter = 0;


// instances de servos
Servo servo1;
Servo servo2;
Servo servo3;

control_servoStruct_t servoStruct = control_setupServoStruct(&servo1, &servo2, &servo3);

control_pins_t pins = control_setupPins(motor1Pin1, motor1Pin2, motor2Pin1, motor2Pin2, servoPin1, servoPin2, servoPin3);


const char *ssid = "Je suis Dieu et dispo";
const char *password = "123456789";

AsyncWebServer server(80);

control_t control_data;
 
void setup()

{ 
  // init servo
  control_setupServos(&servoStruct, &pins);
  // fréquence de PWM
  analogWriteFreq(50);
  // init moteurs
  control_setupMotors(&pins);

  Serial.begin(115200);
  Serial.println("Starting");
 
  espWifi_setup(ssid, password);

  server.on("/patate", HTTP_GET, [](AsyncWebServerRequest *request){
      espWifi_processRequest(request, &control_data);
      if (DEBUG){
        control_printDebug(&control_data);
      }

      request_counter++;
    });
  
  server.begin();

}
 
void loop(){
  if (CONTROL){
    control_update(&control_data, &pins, &servoStruct);
  }
  else{
    control_setNullSpeed(&pins);
  }
/*   if (DEBUG){
    control_printDebug(&control);
  } */
}
