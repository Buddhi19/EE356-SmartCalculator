#include <ArduinoWiFiServer.h>
#include <ESP8266WiFi.h>


void setup()
{
  delay(1000);
  Serial.begin(115200);
  Serial.println("Started");
  scan_wifi();
  connect_wifi();
}

void loop()
{
  digitalWrite(D6, HIGH);
  delay(1000);
  digitalWrite(D6, LOW);
  delay(1000);
}

void scan_wifi(){
  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; ++i)
  {
    Serial.println(WiFi.SSID(i));
  }
}

void connect_wifi(){
  Serial.println("Enter SSID: ");
  while(Serial.available() == 0){
  }
  String ssid = Serial.readString();
  Serial.println("Enter Password: ");
  while(Serial.available() == 0){
  }
  String password = Serial.readString();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to the WiFi network");
}

void post_data(String data){
  //post data to the local server
  
}