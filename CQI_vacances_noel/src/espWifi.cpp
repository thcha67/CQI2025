#include "../lib/espWifi.h"
#include "../lib/espControl.h"
#include "ESP8266WiFi.h"
#include "ESPAsyncWebServer.h"


/// @brief Création du point d'accès wifi, imprime l'adresse IP
/// @param ssid 
/// @param password 
void espWifi_setup(const char *ssid, const char *password){
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
}

/// @brief Traite la requête et met à jour la structure de contrôle
/// @param request 
/// @param control 
void espWifi_processRequest(AsyncWebServerRequest *request, control_t * const control){
  control->direction = (String)(request->getParam("direction")->value());
  control->speed = (uint16_t)(request->getParam("speed")->value().toInt());
  control->correction = (float)(request->getParam("correction")->value().toFloat());
  control->servo1 = (uint16_t)(request->getParam("servo1")->value().toInt());
  control->servo2 = (uint16_t)(request->getParam("servo2")->value().toInt());
  control->servo3 = (uint16_t)(request->getParam("servo3")->value().toInt());
}

void espWifi_processDirectionRequest(AsyncWebServerRequest *request, control_t *control){
  control->direction = (String)(request->getParam("direction")->value());
}

void espWifi_processSpeedRequest(AsyncWebServerRequest *request, control_t *control){
   control->speed = (uint16_t)(request->getParam("speed")->value().toInt());
}

void espWifi_processStateRequest(AsyncWebServerRequest *request, control_t *control){
  control->correction = (float)(request->getParam("correction")->value().toFloat());
  control->servo1 = (uint16_t)(request->getParam("servo1")->value().toInt());
  control->servo2 = (uint16_t)(request->getParam("servo2")->value().toInt());   
  control->servo3 = (uint16_t)(request->getParam("servo3")->value().toInt());
  control->attach_all_servos = (bool)(request->getParam("attach")->value().toInt());
  control->servo_is_modified = true;
}

/*
void espWifi_processClickRequest(AsyncWebServerRequest *request, control_t *control){
  if (request->getParam("btn1")->value().toInt() == 1){
      control->servo_in_sequence = true;
  }
  else if (request->getParam("btn2")->value().toInt() == 1){
      // Ajouter si nécessaire
  }

}
*/