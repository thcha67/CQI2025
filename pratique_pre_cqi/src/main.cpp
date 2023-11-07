#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include <Arduino.h>

#define FREQ 500
#define RESOLUTION 8


void initialize_pins();
void requestHandler(AsyncWebServerRequest *request);
void forward(uint8_t speed, uint8_t correction);
void backward(uint8_t speed, uint8_t correction);


const char* ssid = "patate";  //replace
const char* password =  "321radis"; //replace

AsyncWebServer server(80);
 
void setup()

{

  //initialize_pins();

  Serial.println("Starting");
  digitalWrite(12, LOW);

  delay(5000);
  
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
 
   while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println(WiFi.localIP());
 
  server.on("/patate", HTTP_GET, [](AsyncWebServerRequest *request){
    Serial.println("Okayy");
    // get speed

    // Ajouter fonction pour traiter le pont H
    requestHandler(request);
    
    Serial.println("On");
    digitalWrite(12, HIGH);
    request->send(200);
    });



  server.begin();
  
}
 
void loop(){
}

void forward(uint8_t speed, uint8_t correction)
{
  analogWrite(13, 0);
  // do a pwm for pin 12
  analogWrite(12, speed);
  Serial.print("Speed 12 : ");
  Serial.println(speed);

  analogWrite(15, 0);
  // do a pwm for pin 14
  uint8_t speed2 = (uint8_t)(speed * (correction)/ 255);
  analogWrite(14, speed2);
  Serial.print("Speed 14 : ");
  Serial.println(speed2);
}

void backward(uint8_t speed, uint8_t correction)
{
  analogWrite(13, speed);
  // do a pwm for pin 12
  analogWrite(12, 0);

  analogWrite(15, (uint8_t)(speed * correction / 255));
  // do a pwm for pin 14
  analogWrite(14, 0);
}

void initialize_pins()
{
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(15, OUTPUT);

}

void requestHandler(AsyncWebServerRequest *request){
  
  bool direction = (bool)(request->getParam("direction")->value().toInt());
  bool power = (bool)(request->getParam("power")->value().toInt());
  uint8_t speed = (uint8_t)(request->getParam("speed")->value().toInt());
  uint8_t factor = (uint8_t)(request->getParam("correction")->value().toInt());

  // Debug
  Serial.println(direction);
  Serial.println(power);
  Serial.println(speed);
  Serial.println(factor);

  if (power == 0){
    analogWrite(12, 0);
    analogWrite(13, 0);
    analogWrite(14, 0);
    analogWrite(15, 0);
    return;
  }
  else if (direction == 1){
    forward(speed, factor);
  }
  else{
    backward(speed, factor);
  }

  

}



/*

const char* ssid = "Patate";  // Set the SSID for your ESP32's AP
const char* password = NULL;  // Set a password for your ESP32's AP

AsyncWebServer server(80);

// ...



void setup() {
    // ...

    // Set up the ESP32 as an AP
    WiFi.softAP(ssid, password);

    server.on("/toggleLed", HTTP_GET, [](AsyncWebServerRequest *request){
      static bool ledState = false;
      Serial.print("Led handler entered");
      ledState = !ledState;
      digitalWrite(1, ledState);
      request->send(200);
  });

    // ...
}

void loop(){}

// ...

*/

