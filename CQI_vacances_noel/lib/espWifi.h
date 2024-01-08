#ifndef ESPWIFI
#define ESPWIFI

#include "ESP8266WiFi.h"
#include "ESPAsyncWebServer.h"

#include "espControl.h"

void espWifi_setup(const char *ssid, const char *password);

void espWifi_processRequest(AsyncWebServerRequest *request, control_t *control);

#endif // ESPWIFI