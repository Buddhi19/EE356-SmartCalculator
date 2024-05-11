#include <SPI.h>

#define MOSI_PIN  23 // SPI MOSI pin
#define MISO_PIN  19 // SPI MISO pin
#define SCK_PIN   18 // SPI Clock pin
#define CS_PIN    5  // Chip select pin for ESP32-CAM

void setup() {
  Serial.begin(115200);
  
  pinMode(MOSI_PIN, INPUT);
  pinMode(MISO_PIN, OUTPUT);
  pinMode(SCK_PIN, INPUT);
  pinMode(CS_PIN, INPUT);
  
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN);
}

void loop() {
  if (digitalRead(CS_PIN) == LOW) {
    // ESP32-CAM is selected
    while (SPI.available()) {
      uint8_t data = SPI.transfer(0x00); // Receive data from master
      // Process received data (e.g., save to SD card, display on screen, etc.)
      Serial.write(data); // Example: send data to Serial monitor
    }
  }
  else {
    // ESP32-CAM is not selected
    delay(10); // Wait for next iteration
  }
}
