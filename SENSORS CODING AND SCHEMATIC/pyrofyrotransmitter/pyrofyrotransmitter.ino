#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>
#include <DHT.h>

RF24 radio(9, 8); // CE, CSN
const byte address[6] = "00001";

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  dht.begin();
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  
  if (!isnan(t) && !isnan(h)) {
    char dataToSend[32];
    sprintf(dataToSend, "%.2f,%.2f", t, h);
    
    radio.write(dataToSend, sizeof(dataToSend));
    delay(1000);
  }
}
