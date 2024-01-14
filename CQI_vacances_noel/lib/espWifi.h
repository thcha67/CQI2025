#ifndef ESPWIFI
#define ESPWIFI

#include "ESP8266WiFi.h"
#include "ESPAsyncWebServer.h"

#include "espControl.h"

void espWifi_setup(const char *ssid, const char *password);

void espWifi_processRequest(AsyncWebServerRequest *request, control_t * const control); // ancienne fonction (n'est plus utilisée normalement)

void espWifi_processDirectionRequest(AsyncWebServerRequest *request, control_t *control);

void espWifi_processSpeedRequest(AsyncWebServerRequest *request, control_t *control);

void espWifi_processStateRequest(AsyncWebServerRequest *request, control_t *control);

void espWifi_processClickRequest(AsyncWebServerRequest *request, control_t *control);

#endif // ESPWIFI