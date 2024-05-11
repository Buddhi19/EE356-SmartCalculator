#include <ESP8266HTTPClient.h>
#include <ArduinoWiFiServer.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <WiFiClient.h>

String serverAddress = "192.168.1.4";

void setup()
{
  delay(1000);
  Serial.begin(115200);
  Serial.println("Started");
  connect_wifi();
  // post_data("Hello World");
}

void loop()
{
  // while (Serial.available() == 0)
  // {
  // }
  // String data = Serial.readString();
  // post_data(data);
  receive_data();
}


void connect_wifi(){
  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; ++i)
  {
    Serial.println(WiFi.SSID(i));
  }

  Serial.println("Enter SSID: ");
  while(Serial.available() == 0){
  }
  String ssid = Serial.readString();
  Serial.println("Enter Password: ");
  while(Serial.available() == 0){
  }
  String password = Serial.readString();
  WiFi.begin(ssid, password);
  int t = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting...");
    t++;
    if(t > 10){
      Serial.println("Connection failed");
      return connect_wifi();
    }
  }
  Serial.println("Connected to the WiFi network");
}

void post_data(String data){
  //post data to the local server
  int port = 80;

  StaticJsonDocument<200> doc;
  doc["data"] = data;
  String json_data;
  serializeJson(doc, json_data);

  WiFiClient client;
  HTTPClient http;
  http.begin(client,"http://" + serverAddress + ":" + String(port) + "/json1");
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(json_data);

  if (httpResponseCode > 0)
  {
    String response = http.getString();
    Serial.println(httpResponseCode);
    Serial.println(response);
  }
  else
  {
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}

void receive_data(){
  //get data from the local server
  int port = 80;
  WiFiClient client;
  HTTPClient http;
  http.begin(client,"http://" + serverAddress + ":" + String(port) + "/json2");
  int httpResponseCode = http.GET();

  if (httpResponseCode > 0)
  {
    String response = http.getString();
    Serial.println(httpResponseCode);
    Serial.println(response);
  }
  else
  {
    Serial.print("Error on sending GET: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}