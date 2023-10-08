#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>
#include <WiFiClientSecure.h>
#include <DHT.h>

RF24 radio(9, 8);
const byte address[6] = "00001";

const char* ssid = "WIFI SSID";
const char* password = "WIFI PASSWORD";
const char* host = "script.google.com";
const int httpsPort = 443;
WiFiClientSecure client;

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

String GAS_ID = "YourSheetsGASID";

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(1, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  
  dht.begin();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  client.setInsecure();
}

void loop() {
  if (radio.available()) {
    char dataReceived[32] = "";
    radio.read(&dataReceived, sizeof(dataReceived));
    Serial.println(dataReceived);
    
    float t, h;
    if (sscanf(dataReceived, "%f,%f", &t, &h) == 2) {
      sendData(t, h);
    }
  }
}

void sendData(float tem, float hum) {
  String url = "/macros/s/" + GAS_ID + "/exec?t=" + String(tem) + "&h=" + String(hum);
  Serial.print("Requesting URL: ");
  Serial.println(url);

  if (!client.connect(host, httpsPort)) {
    Serial.println("Connection to Google Sheets failed");
    return;
  }

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "User-Agent: ArduinoWiFi/1.1\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("Request sent");

  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("Headers received");
      break;
    }
  }

  String response = client.readString();
  Serial.println("Response from Google Sheets:");
  Serial.println(response);

  client.stop();
  Serial.println("Connection closed");
}
